"""
Report Summarizer (hybrid approach)

Input:  report_text (str) - raw text extracted from a medical report
Output: {
    "summary": str,
    "flags": list[str],
    "extracted_values": dict,   # bonus field beyond the original API_CONTRACT.md
}                               # shape -- additive, doesn't break existing callers

Stage 1 (rule-based, always runs): regex-extract known lab values from the
report text and compare against reference ranges in data/lab_reference_ranges.json.
This is deterministic and never hallucinates a number -- important for medical data.

Stage 2 (Claude API, best-effort): turn the extracted values + flags + raw text
into a short plain-language narrative summary for a patient/doctor. If no API
key is configured, or the request fails, we fall back to a rule-based summary
built directly from the flags -- nothing in this module ever *requires* the
network to produce a usable result.
"""

import json
import os
import re

from utils.claude_client import get_narrative

REFERENCE_PATH = os.path.join(os.path.dirname(__file__), "data", "lab_reference_ranges.json")

# Maps a reference-range key to regex patterns that might *name* it in report
# text -- these only match the label, not the value. Real lab report PDFs
# (especially table-formatted ones, once extracted as plain text) almost
# never put a label and its number on the same line -- there's usually a
# methodology annotation in between, e.g.:
#
#   Haemoglobin
#   Cyanide free
#   12
#   gm/dl
#   12.0-15.0
#
# So extraction works in two steps: find a line naming the field, then look
# at the next few lines for the first one that's just a number (see
# extract_lab_values below). Aliases also cover regional terminology common
# in Indian lab reports (Haemoglobin, TLC, SGOT/SGPT) alongside the more
# generic US-style names.
FIELD_LABEL_PATTERNS = {
    "hemoglobin": [r"h(?:a)?emoglobin"],
    "wbc": [r"\bwbc\b", r"white\s*blood\s*cell", r"\btlc\b", r"total\s*leu[ck]ocyte\s*count"],
    "platelets": [r"platelet"],
    "fasting_sugar": [r"fasting\s*blood\s*sugar", r"\bfbs\b", r"blood\s*sugar"],
    "total_cholesterol": [r"total\s*cholesterol"],
    "ldl": [r"\bldl\b"],
    "hdl": [r"\bhdl\b"],
    "triglycerides": [r"triglycerides"],
    "heart_rate": [r"heart\s*rate"],
    "creatinine": [r"creatinine"],
    "alt": [r"\balt\b", r"\bsgpt\b", r"alanine\s*(?:transaminase|aminotransferase)"],
    "ast": [r"\bast\b", r"\bsgot\b", r"aspartate\s*(?:transaminase|aminotransferase)"],
    "tsh": [r"\btsh\b"],
    # NOTE: real HbA1c interpretation is categorical (normal <5.7%, prediabetes
    # 5.7-6.4%, diabetes >=6.5%), not a simple low/high band like the other
    # fields here. We're using the same low/high mechanism for consistency in
    # this MVP, so "high" for HbA1c really means "at or above normal" -- call
    # this out if it comes up in a demo/interview.
    "hba1c": [r"hba1c", r"glycated\s*h(?:a)?emoglobin"],
}

# A field's value is the first standalone number found on or after its label
# line. Requiring the number to be at the START of the line (for lookahead
# lines) is what lets us skip over methodology annotations like "Calculated"
# or "Flowcytometry", which never start with a digit.
NUMBER_RE = re.compile(r"-?\d+\.?\d*")

# WBC and Platelet counts are very commonly reported in *thousands* per uL on
# real lab report templates (units like "th/cumm", "thou/uL", "x10^3/uL",
# "K/uL") even though lab_reference_ranges.json's ranges are in absolute
# counts per uL. Missing this turns a perfectly normal 6.33 th/cumm into a
# false "Low WBC Count (6.33)" flag. We check the unit text right after the
# matched number and scale up by 1000 if it looks like a thousands unit.
COUNT_FIELDS_REPORTED_IN_THOUSANDS = {"wbc", "platelets"}
THOUSANDS_UNIT_RE = re.compile(r"(thou|th|k)(?:\b|/)|x\s*10\^?\s*3", re.IGNORECASE)


def _load_reference_ranges() -> dict:
    if os.path.exists(REFERENCE_PATH):
        with open(REFERENCE_PATH) as f:
            return json.load(f)
    return {}


def _find_value_near_label(lines: list, label_patterns: list, lookahead: int = 4):
    """Find the first line matching any of label_patterns, then return
    (value, unit_hint) from the first number on that same line, or on one of
    the next `lookahead` lines (whichever comes first). unit_hint is
    whatever text immediately follows the matched number's line -- usually
    the units column in a table-style report. Returns (None, None) if the
    label isn't found, or is found but no nearby number is."""
    for i, line in enumerate(lines):
        if not any(re.search(p, line, re.IGNORECASE) for p in label_patterns):
            continue
        same_line_match = NUMBER_RE.search(line)
        if same_line_match:
            return float(same_line_match.group()), line
        for j in range(i + 1, min(i + 1 + lookahead, len(lines))):
            next_line_match = NUMBER_RE.match(lines[j])
            if next_line_match:
                unit_hint = lines[j + 1] if j + 1 < len(lines) else ""
                return float(next_line_match.group()), unit_hint
        # This occurrence of the label had no number nearby (e.g. mentioned
        # in a comment paragraph) -- keep scanning in case it appears again
        # later, in an actual results row.
    return None, None


def extract_lab_values(report_text: str) -> dict:
    """Stage 1: pull out any recognized lab values from free text."""
    lines = [line.strip() for line in report_text.splitlines() if line.strip()]
    found = {}
    for key, label_patterns in FIELD_LABEL_PATTERNS.items():
        value, unit_hint = _find_value_near_label(lines, label_patterns)
        if value is None:
            continue
        if key in COUNT_FIELDS_REPORTED_IN_THOUSANDS and unit_hint and THOUSANDS_UNIT_RE.search(unit_hint):
            value *= 1000
        found[key] = value
    return found


def flag_abnormal_values(extracted_values: dict, reference_ranges: dict) -> list:
    """Compare extracted values against reference ranges and produce
    human-readable flags for anything outside normal range."""
    flags = []
    for key, value in extracted_values.items():
        ref = reference_ranges.get(key)
        if not ref:
            continue
        label = ref.get("label", key)
        if value < ref["low"]:
            flags.append(f"Low {label} ({value} {ref['unit']}, normal range {ref['low']}-{ref['high']})")
        elif value > ref["high"]:
            flags.append(f"High {label} ({value} {ref['unit']}, normal range {ref['low']}-{ref['high']})")
    return flags


def _fallback_summary(flags: list, extracted_values: dict) -> str:
    """Used when the Claude API isn't available. Deliberately plain -- this is
    a safety net, not a replacement for the narrative summary."""
    if not extracted_values:
        return "No recognized lab values found in this report. Manual review recommended."
    if not flags:
        return "All extracted values are within normal reference ranges."
    return "Findings outside normal range: " + "; ".join(flags) + ". Please consult your doctor."


SYSTEM_PROMPT = (
    "You are a medical report summarization assistant used inside a hospital "
    "management system. You are given ALREADY-EXTRACTED, verified lab values "
    "and flags -- never invent or alter any number yourself. Write a short "
    "(3-5 sentence) plain-language summary suitable for both a patient and a "
    "doctor skimming a chart. Mention flagged values first, in plain terms, "
    "then note what's normal. End with a brief, non-alarming next-step "
    "suggestion (e.g. 'discuss with your doctor') if there are flags. Do not "
    "give a diagnosis. Do not add medical advice beyond suggesting follow-up."
)


def summarize_report(report_text: str) -> dict:
    reference_ranges = _load_reference_ranges()
    extracted_values = extract_lab_values(report_text)
    flags = flag_abnormal_values(extracted_values, reference_ranges)

    user_prompt = (
        f"Raw report text:\n{report_text}\n\n"
        f"Extracted values: {json.dumps(extracted_values)}\n"
        f"Flags: {json.dumps(flags)}\n\n"
        "Write the summary now."
    )
    narrative = get_narrative(SYSTEM_PROMPT, user_prompt)
    summary = narrative if narrative else _fallback_summary(flags, extracted_values)

    return {"summary": summary, "flags": flags, "extracted_values": extracted_values}


if __name__ == "__main__":
    sample = "Hemoglobin: 11.2 g/dL, Platelets: 250000, Blood Sugar: 95 mg/dL"
    print(json.dumps(summarize_report(sample), indent=2))