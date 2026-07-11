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

# Maps a reference-range key to the regex patterns that might name it in raw
# report text. Multiple aliases per key since different report templates /
# hospitals phrase things differently (e.g. "WBC Count" vs "White Blood Cells").
FIELD_PATTERNS = {
    "hemoglobin": [r"hemoglobin\s*[:\-]?\s*([\d.]+)"],
    "wbc": [r"wbc\s*(?:count)?\s*[:\-]?\s*([\d.]+)", r"white blood cell[s]?\s*[:\-]?\s*([\d.]+)"],
    "platelets": [r"platelet[s]?\s*(?:count)?\s*[:\-]?\s*([\d.]+)"],
    "fasting_sugar": [r"(?:fasting\s*)?blood\s*sugar\s*[:\-]?\s*([\d.]+)"],
    "total_cholesterol": [r"total\s*cholesterol\s*[:\-]?\s*([\d.]+)"],
    "ldl": [r"\bldl\s*[:\-]?\s*([\d.]+)"],
    "hdl": [r"\bhdl\s*[:\-]?\s*([\d.]+)"],
    "triglycerides": [r"triglycerides\s*[:\-]?\s*([\d.]+)"],
    "heart_rate": [r"heart\s*rate\s*[:\-]?\s*([\d.]+)"],
    "creatinine": [r"creatinine\s*[:\-]?\s*([\d.]+)"],
    "alt": [r"\balt\s*[:\-]?\s*([\d.]+)", r"alanine\s*(?:transaminase|aminotransferase)\s*[:\-]?\s*([\d.]+)"],
    "ast": [r"\bast\s*[:\-]?\s*([\d.]+)", r"aspartate\s*(?:transaminase|aminotransferase)\s*[:\-]?\s*([\d.]+)"],
    "tsh": [r"\btsh\s*[:\-]?\s*([\d.]+)"],
    # NOTE: real HbA1c interpretation is categorical (normal <5.7%, prediabetes
    # 5.7-6.4%, diabetes >=6.5%), not a simple low/high band like the other
    # fields here. We're using the same low/high mechanism for consistency in
    # this MVP, so "high" for HbA1c really means "at or above normal" -- call
    # this out if it comes up in a demo/interview.
    "hba1c": [r"hba1c\s*[:\-]?\s*([\d.]+)", r"glycated\s*hemoglobin\s*[:\-]?\s*([\d.]+)"],
}


def _load_reference_ranges() -> dict:
    if os.path.exists(REFERENCE_PATH):
        with open(REFERENCE_PATH) as f:
            return json.load(f)
    return {}


def extract_lab_values(report_text: str) -> dict:
    """Stage 1: pull out any recognized lab values from free text."""
    text = report_text.lower()
    found = {}
    for key, patterns in FIELD_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                found[key] = float(match.group(1))
                break
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