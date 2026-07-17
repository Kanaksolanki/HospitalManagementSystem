# """
# Report Summarizer (hybrid approach)

# Input:  report_text (str) - raw text extracted from a medical report
# Output: {
#     "summary": str,
#     "flags": list[str],
#     "extracted_values": dict,   # bonus field beyond the original API_CONTRACT.md
# }                               # shape -- additive, doesn't break existing callers

# Stage 1 (rule-based, always runs): regex-extract known lab values from the
# report text and compare against reference ranges in data/lab_reference_ranges.json.
# This is deterministic and never hallucinates a number -- important for medical data.

# Stage 2 (Claude API, best-effort): turn the extracted values + flags + raw text
# into a short plain-language narrative summary for a patient/doctor. If no API
# key is configured, or the request fails, we fall back to a rule-based summary
# built directly from the flags -- nothing in this module ever *requires* the
# network to produce a usable result.
# """

# import json
# import os
# import re

# # from utils.claude_client import get_narrative

# REFERENCE_PATH = os.path.join(os.path.dirname(__file__), "data", "lab_reference_ranges.json")

# # Maps a reference-range key to regex patterns that might *name* it in report
# # text -- these only match the label, not the value. Real lab report PDFs
# # (especially table-formatted ones, once extracted as plain text) almost
# # never put a label and its number on the same line -- there's usually a
# # methodology annotation in between, e.g.:
# #
# #   Haemoglobin
# #   Cyanide free
# #   12
# #   gm/dl
# #   12.0-15.0
# #
# # So extraction works in two steps: find a line naming the field, then look
# # at the next few lines for the first one that's just a number (see
# # extract_lab_values below). Aliases also cover regional terminology common
# # in Indian lab reports (Haemoglobin, TLC, SGOT/SGPT) alongside the more
# # generic US-style names.
# FIELD_LABEL_PATTERNS = {
#     "hemoglobin": [r"h(?:a)?emoglobin"],
#     "rbc": [r"\brbc\b", r"red\s*blood\s*cell\s*count"],
#     "hematocrit": [r"h(?:a)?ematocrit", r"\bpcv\b", r"packed\s*cell\s*volume"],
#     "mcv": [r"\bmcv\b", r"mean\s*corpuscular\s*volume"],
#     "mch": [r"\bmch\b(?!c)", r"mean\s*corpuscular\s*h(?:a)?emoglobin(?!\s*concentration)"],
#     "mchc": [r"\bmchc\b", r"mean\s*corpuscular\s*h(?:a)?emoglobin\s*concentration"],
#     "wbc": [r"\bwbc\b", r"white\s*blood\s*cell", r"\btlc\b", r"total\s*leu[ck]ocyte\s*count"],
#     "platelets": [r"platelet"],
#     "esr": [r"\besr\b", r"erythrocyte\s*sedimentation\s*rate"],
#     "crp": [r"\bcrp\b", r"c[\s-]*reactive\s*protein"],
#     "fasting_sugar": [r"fasting\s*blood\s*sugar", r"\bfbs\b", r"fasting\s*(?:plasma\s*)?glucose"],
#     "post_prandial_sugar": [r"post\s*prandial", r"\bppbs\b", r"pp\s*blood\s*sugar"],
#     "random_blood_sugar": [r"random\s*blood\s*sugar", r"\brbs\b"],
#     "hba1c": [r"hba1c", r"glycated\s*h(?:a)?emoglobin"],
#     "total_cholesterol": [r"total\s*cholesterol"],
#     "ldl": [r"\bldl\b"],
#     "hdl": [r"\bhdl\b"],
#     "vldl": [r"\bvldl\b"],
#     "triglycerides": [r"triglycerides"],
#     "heart_rate": [r"heart\s*rate", r"\bpulse\b"],
#     "spo2": [r"\bspo2\b", r"oxygen\s*saturation"],
#     "creatinine": [r"creatinine"],
#     "urea": [r"\burea\b", r"blood\s*urea"],
#     "uric_acid": [r"uric\s*acid"],
#     "sodium": [r"\bsodium\b", r"\bna\+?\b"],
#     "potassium": [r"\bpotassium\b", r"\bk\+?\b"],
#     "calcium": [r"\bcalcium\b"],
#     "alt": [r"\balt\b", r"\bsgpt\b", r"alanine\s*(?:transaminase|aminotransferase)"],
#     "ast": [r"\bast\b", r"\bsgot\b", r"aspartate\s*(?:transaminase|aminotransferase)"],
#     "alp": [r"\balp\b", r"alkaline\s*phosphatase"],
#     "total_bilirubin": [r"total\s*bilirubin"],
#     "direct_bilirubin": [r"direct\s*bilirubin"],
#     "albumin": [r"\balbumin\b"],
#     "total_protein": [r"total\s*protein"],
#     "tsh": [r"\btsh\b"],
#     "t3": [r"\bt3\b(?!\s*t4)", r"triiodothyronine"],
#     "t4": [r"\bt4\b", r"thyroxine"],
#     "vitamin_d": [r"vitamin\s*d", r"25[\s-]*oh\s*vitamin\s*d"],
#     "vitamin_b12": [r"vitamin\s*b[\s-]*12", r"\bcobalamin\b"],
#     "iron": [r"\bserum\s*iron\b", r"\biron\b(?!\s*binding)"],
#     "ferritin": [r"ferritin"],
# }

# # A field's value is the first standalone number found on or after its label
# # line. Requiring the number to be at the START of the line (for lookahead
# # lines) is what lets us skip over methodology annotations like "Calculated"
# # or "Flowcytometry", which never start with a digit.
# NUMBER_RE = re.compile(r"-?\d+\.?\d*")

# # WBC and Platelet counts are very commonly reported in *thousands* per uL on
# # real lab report templates (units like "th/cumm", "thou/uL", "x10^3/uL",
# # "K/uL") even though lab_reference_ranges.json's ranges are in absolute
# # counts per uL. Missing this turns a perfectly normal 6.33 th/cumm into a
# # false "Low WBC Count (6.33)" flag. We check the unit text right after the
# # matched number and scale up by 1000 if it looks like a thousands unit.
# COUNT_FIELDS_REPORTED_IN_THOUSANDS = {"wbc", "platelets"}
# THOUSANDS_UNIT_RE = re.compile(r"(thou|th|k)(?:\b|/)|x\s*10\^?\s*3", re.IGNORECASE)


# def _load_reference_ranges() -> dict:
#     if os.path.exists(REFERENCE_PATH):
#         with open(REFERENCE_PATH) as f:
#             return json.load(f)
#     return {}


# def _find_value_near_label(lines: list, label_patterns: list, lookahead: int = 4):
#     """Find the first line matching any of label_patterns, then return
#     (value, unit_hint). Two cases are handled:
#     1. Inline format ("Hemoglobin: 11.2 g/dL") -- take the first number on
#        the same line that is NOT part of a reference-range pattern like
#        "12.0-15.0" (so we don't accidentally grab a range boundary).
#     2. Table format (label on its own line, value on a line below) -- look
#        at the next `lookahead` lines for the first one that's just a bare
#        number by itself.
#     Returns (None, None) if the label isn't found, or is found but no
#     value can be reliably identified."""
#     standalone_number_re = re.compile(r"^-?\d+\.?\d*$")
#     range_re = re.compile(r"\d+\.?\d*\s*-\s*\d+\.?\d*")

#     for i, line in enumerate(lines):
#         if not any(re.search(p, line, re.IGNORECASE) for p in label_patterns):
#             continue

#         # Case 1: inline. Skip any number that's part of a "X-Y" range.
#         range_spans = [m.span() for m in range_re.finditer(line)]
#         for num_match in NUMBER_RE.finditer(line):
#             if any(start <= num_match.start() < end for start, end in range_spans):
#                 continue
#             return float(num_match.group()), line

#         # Case 2: table format -- value on a line below the label.
#         for j in range(i + 1, min(i + 1 + lookahead, len(lines))):
#             candidate = lines[j].strip()
#             match = standalone_number_re.match(candidate)
#             if match:
#                 unit_hint = lines[j + 1] if j + 1 < len(lines) else ""
#                 return float(match.group()), unit_hint

#     return None, None


# def extract_lab_values(report_text: str) -> dict:
#     """Stage 1: pull out any recognized lab values from free text."""
#     lines = [line.strip() for line in report_text.splitlines() if line.strip()]
#     found = {}
#     for key, label_patterns in FIELD_LABEL_PATTERNS.items():
#         value, unit_hint = _find_value_near_label(lines, label_patterns)
#         if value is None:
#             continue
#         if key in COUNT_FIELDS_REPORTED_IN_THOUSANDS and unit_hint and THOUSANDS_UNIT_RE.search(unit_hint):
#             value *= 1000
#         found[key] = value
#     return found


# def flag_abnormal_values(extracted_values: dict, reference_ranges: dict) -> list:
#     """Compare extracted values against reference ranges and produce
#     human-readable flags for anything outside normal range."""
#     flags = []
#     for key, value in extracted_values.items():
#         ref = reference_ranges.get(key)
#         if not ref:
#             continue
#         label = ref.get("label", key)
#         if value < ref["low"]:
#             flags.append(f"Low {label} ({value} {ref['unit']}, normal range {ref['low']}-{ref['high']})")
#         elif value > ref["high"]:
#             flags.append(f"High {label} ({value} {ref['unit']}, normal range {ref['low']}-{ref['high']})")
#     return flags


# def _fallback_summary(flags: list, extracted_values: dict) -> str:
#     """Used when the Claude API isn't available. Deliberately plain -- this is
#     a safety net, not a replacement for the narrative summary."""
#     if not extracted_values:
#         return "No recognized lab values found in this report. Manual review recommended."
#     if not flags:
#         return "All extracted values are within normal reference ranges."
#     return "Findings outside normal range: " + "; ".join(flags) + ". Please consult your doctor."


# SYSTEM_PROMPT = (
#     "You are a medical report summarization assistant used inside a hospital "
#     "management system. You are given ALREADY-EXTRACTED, verified lab values "
#     "and flags -- never invent or alter any number yourself. Write a short "
#     "(3-5 sentence) plain-language summary suitable for both a patient and a "
#     "doctor skimming a chart. Mention flagged values first, in plain terms, "
#     "then note what's normal. End with a brief, non-alarming next-step "
#     "suggestion (e.g. 'discuss with your doctor') if there are flags. Do not "
#     "give a diagnosis. Do not add medical advice beyond suggesting follow-up."
# )


# def summarize_report(report_text: str) -> dict:
#     reference_ranges = _load_reference_ranges()
#     extracted_values = extract_lab_values(report_text)
#     flags = flag_abnormal_values(extracted_values, reference_ranges)

#     user_prompt = (
#         f"Raw report text:\n{report_text}\n\n"
#         f"Extracted values: {json.dumps(extracted_values)}\n"
#         f"Flags: {json.dumps(flags)}\n\n"
#         "Write the summary now."
#     )
#     narrative = get_narrative(SYSTEM_PROMPT, user_prompt)
#     summary = narrative if narrative else _fallback_summary(flags, extracted_values)

#     return {"summary": summary, "flags": flags, "extracted_values": extracted_values}


# # if __name__ == "__main__":
# #     sample = "Hemoglobin: 11.2 g/dL, Platelets: 250000, Blood Sugar: 95 mg/dL"
# #     print(json.dumps(summarize_report(sample), indent=2))

# if __name__ == "__main__":
#     sample = """Hemoglobin
# Cyanide free
# 12.0
# gm/dl
# 12.0-15.0
# WBC Count
# 6330
# /cumm
# 4000-11000
# Platelet Count
# 250000
# /cumm
# 150000-410000"""
#     print(json.dumps(summarize_report(sample), indent=2))




"""
Report Summarizer (rule-based)

Input:  report_text (str) - raw text extracted from a medical report
Output: {
    "summary": str,
    "flags": list[str],
    "extracted_values": dict,
}

Purely rule-based, no LLM involved: regex-extracts known lab values from the
report text, compares them against reference ranges in
data/lab_reference_ranges.json, and builds a plain-language narrative summary
using a small built-in knowledge base of what each abnormal value commonly
indicates. Deterministic and never hallucinates a number -- important for
medical data.
"""

import json
import os
import re

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
    "rbc": [r"\brbc\b", r"red\s*blood\s*cell\s*count"],
    "hematocrit": [r"h(?:a)?ematocrit", r"\bpcv\b", r"packed\s*cell\s*volume"],
    "mcv": [r"\bmcv\b", r"mean\s*corpuscular\s*volume"],
    "mch": [r"\bmch\b(?!c)", r"mean\s*corpuscular\s*h(?:a)?emoglobin(?!\s*concentration)"],
    "mchc": [r"\bmchc\b", r"mean\s*corpuscular\s*h(?:a)?emoglobin\s*concentration"],
    "wbc": [r"\bwbc\b", r"white\s*blood\s*cell", r"\btlc\b", r"total\s*leu[ck]ocyte\s*count"],
    "platelets": [r"platelet"],
    "esr": [r"\besr\b", r"erythrocyte\s*sedimentation\s*rate"],
    "crp": [r"\bcrp\b", r"c[\s-]*reactive\s*protein"],
    "fasting_sugar": [r"fasting\s*blood\s*sugar", r"\bfbs\b", r"fasting\s*(?:plasma\s*)?glucose"],
    "post_prandial_sugar": [r"post\s*prandial", r"\bppbs\b", r"pp\s*blood\s*sugar"],
    "random_blood_sugar": [r"random\s*blood\s*sugar", r"\brbs\b"],
    "hba1c": [r"hba1c", r"glycated\s*h(?:a)?emoglobin"],
    "total_cholesterol": [r"total\s*cholesterol"],
    "ldl": [r"\bldl\b"],
    "hdl": [r"\bhdl\b"],
    "vldl": [r"\bvldl\b"],
    "triglycerides": [r"triglycerides"],
    "heart_rate": [r"heart\s*rate", r"\bpulse\b"],
    "spo2": [r"\bspo2\b", r"oxygen\s*saturation"],
    "creatinine": [r"creatinine"],
    "urea": [r"\burea\b", r"blood\s*urea"],
    "uric_acid": [r"uric\s*acid"],
    "sodium": [r"\bsodium\b", r"\bna\+?\b"],
    "potassium": [r"\bpotassium\b", r"\bk\+?\b"],
    "calcium": [r"\bcalcium\b"],
    "alt": [r"\balt\b", r"\bsgpt\b", r"alanine\s*(?:transaminase|aminotransferase)"],
    "ast": [r"\bast\b", r"\bsgot\b", r"aspartate\s*(?:transaminase|aminotransferase)"],
    "alp": [r"\balp\b", r"alkaline\s*phosphatase"],
    "total_bilirubin": [r"total\s*bilirubin"],
    "direct_bilirubin": [r"direct\s*bilirubin"],
    "albumin": [r"\balbumin\b"],
    "total_protein": [r"total\s*protein"],
    "tsh": [r"\btsh\b"],
    "t3": [r"\bt3\b(?!\s*t4)", r"triiodothyronine"],
    "t4": [r"\bt4\b", r"thyroxine"],
    "vitamin_d": [r"vitamin\s*d", r"25[\s-]*oh\s*vitamin\s*d"],
    "vitamin_b12": [r"vitamin\s*b[\s-]*12", r"\bcobalamin\b"],
    "iron": [r"\bserum\s*iron\b", r"\biron\b(?!\s*binding)"],
    "ferritin": [r"ferritin"],
}

# A field's value is the first standalone number found on or after its label
# line, OR the first non-range number found inline on the same line.
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
    (value, unit_hint). Two cases are handled:
    1. Inline format ("Hemoglobin: 11.2 g/dL") -- take the first number on
       the same line that is NOT part of a reference-range pattern like
       "12.0-15.0" (so we don't accidentally grab a range boundary).
    2. Table format (label on its own line, value on a line below) -- look
       at the next `lookahead` lines for the first one that's just a bare
       number by itself.
    Returns (None, None) if the label isn't found, or is found but no
    value can be reliably identified."""
    standalone_number_re = re.compile(r"^-?\d+\.?\d*$")
    range_re = re.compile(r"\d+\.?\d*\s*-\s*\d+\.?\d*")

    for i, line in enumerate(lines):
        if not any(re.search(p, line, re.IGNORECASE) for p in label_patterns):
            continue

        # Case 1: inline. Skip any number that's part of a "X-Y" range.
        range_spans = [m.span() for m in range_re.finditer(line)]
        for num_match in NUMBER_RE.finditer(line):
            if any(start <= num_match.start() < end for start, end in range_spans):
                continue
            return float(num_match.group()), line

        # Case 2: table format -- value on a line below the label.
        for j in range(i + 1, min(i + 1 + lookahead, len(lines))):
            candidate = lines[j].strip()
            match = standalone_number_re.match(candidate)
            if match:
                unit_hint = lines[j + 1] if j + 1 < len(lines) else ""
                return float(match.group()), unit_hint

    return None, None


def extract_lab_values(report_text: str) -> dict:
    """Pull out any recognized lab values from free text."""
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


# Plain-language explanations for common flagged values -- purely rule-based,
# no LLM involved. Each entry explains what a low/high result on that field
# commonly indicates, phrased carefully to inform without diagnosing.
PLAIN_LANGUAGE_NOTES = {
    "hemoglobin": {
        "low": "can be a sign of anemia, and is often linked to iron deficiency, poor diet, or blood loss",
        "high": "can occur with dehydration, smoking, or certain lung/heart conditions",
    },
    "rbc": {
        "low": "may point to anemia or a blood loss issue",
        "high": "can be linked to dehydration or, less commonly, a bone marrow condition",
    },
    "hematocrit": {
        "low": "often accompanies low hemoglobin and can indicate anemia or blood loss",
        "high": "can occur with dehydration or certain lung/heart conditions",
    },
    "mcv": {
        "low": "suggests smaller-than-average red blood cells, often linked to iron deficiency",
        "high": "suggests larger-than-average red blood cells, sometimes linked to vitamin B12 or folate deficiency",
    },
    "mch": {
        "low": "often accompanies iron-deficiency anemia",
        "high": "can be linked to vitamin B12 or folate deficiency",
    },
    "mchc": {
        "low": "can indicate iron-deficiency anemia",
        "high": "is less common and may need lab confirmation to rule out a testing artifact",
    },
    "wbc": {
        "low": "can indicate a weakened immune response or be a side effect of certain medications",
        "high": "often signals the body is fighting an infection or inflammation",
    },
    "platelets": {
        "low": "may increase bleeding or bruising risk and can be linked to infections or certain medications",
        "high": "can be linked to inflammation, iron deficiency, or in rare cases a bone marrow condition",
    },
    "esr": {
        "low": "is uncommon and usually not a concern on its own",
        "high": "is a general marker of inflammation somewhere in the body, not specific to one condition",
    },
    "crp": {
        "low": "is expected and not a concern",
        "high": "indicates active inflammation or infection somewhere in the body",
    },
    "fasting_sugar": {
        "low": "may cause symptoms like shakiness, sweating, or dizziness if it drops further",
        "high": "is a key marker doctors use to screen for prediabetes or diabetes",
    },
    "post_prandial_sugar": {
        "low": "may cause symptoms like shakiness or dizziness if it drops further",
        "high": "can indicate the body isn't processing sugar from meals efficiently",
    },
    "random_blood_sugar": {
        "low": "may cause symptoms like shakiness, sweating, or dizziness",
        "high": "warrants a follow-up fasting or HbA1c test to screen for diabetes",
    },
    "hba1c": {
        "low": "is not typically a concern",
        "high": "reflects higher average blood sugar over the past ~3 months and is used to screen for diabetes",
    },
    "total_cholesterol": {
        "low": "is uncommon and usually not a concern on its own",
        "high": "is associated with increased risk of heart disease over time",
    },
    "ldl": {
        "low": "is generally favorable for heart health",
        "high": "is often called 'bad cholesterol' and raises cardiovascular risk",
    },
    "hdl": {
        "low": "is often called 'good cholesterol' — being low can raise heart disease risk",
        "high": "is generally considered protective for heart health",
    },
    "vldl": {
        "low": "is not typically a concern",
        "high": "often rises alongside high triglycerides and is linked to heart disease risk",
    },
    "triglycerides": {
        "low": "is uncommon and usually not a concern on its own",
        "high": "is linked to higher risk of heart disease, especially alongside high LDL",
    },
    "heart_rate": {
        "low": "can be normal in athletes, but may also indicate a heart rhythm issue",
        "high": "can be due to stress, caffeine, dehydration, fever, or a heart rhythm issue",
    },
    "spo2": {
        "low": "means blood oxygen is below the healthy range and may need prompt medical attention",
        "high": "is not a typical clinical concern (readings don't usually exceed 100%)",
    },
    "creatinine": {
        "low": "is uncommon and usually not clinically significant",
        "high": "can indicate reduced kidney function",
    },
    "urea": {
        "low": "can be linked to a low-protein diet or liver issues",
        "high": "can indicate reduced kidney function or dehydration",
    },
    "uric_acid": {
        "low": "is uncommon and usually not a concern on its own",
        "high": "is linked to gout and kidney stone risk",
    },
    "sodium": {
        "low": "can cause confusion or weakness and may need prompt medical attention if severe",
        "high": "is often linked to dehydration",
    },
    "potassium": {
        "low": "can cause muscle weakness or heart rhythm issues if significant",
        "high": "can affect heart rhythm and may need prompt medical attention if significant",
    },
    "calcium": {
        "low": "can cause muscle cramps or tingling and may relate to vitamin D or parathyroid issues",
        "high": "can be linked to parathyroid issues or excess vitamin D",
    },
    "alt": {
        "low": "is not typically a concern",
        "high": "can indicate liver strain or inflammation",
    },
    "ast": {
        "low": "is not typically a concern",
        "high": "can indicate liver or muscle strain",
    },
    "alp": {
        "low": "is uncommon and usually not a concern on its own",
        "high": "can be linked to liver or bone conditions",
    },
    "total_bilirubin": {
        "low": "is not typically a concern",
        "high": "can indicate liver strain or a bile-flow issue, and may relate to jaundice",
    },
    "direct_bilirubin": {
        "low": "is not typically a concern",
        "high": "often points to a liver or bile-duct issue specifically",
    },
    "albumin": {
        "low": "can indicate liver or kidney issues, or poor nutrition",
        "high": "is uncommon and often related to dehydration",
    },
    "total_protein": {
        "low": "can be linked to liver or kidney issues, or poor nutrition",
        "high": "can be linked to chronic inflammation or, rarely, a bone marrow condition",
    },
    "tsh": {
        "low": "can indicate an overactive thyroid (hyperthyroidism)",
        "high": "can indicate an underactive thyroid (hypothyroidism)",
    },
    "t3": {
        "low": "can indicate an underactive thyroid",
        "high": "can indicate an overactive thyroid",
    },
    "t4": {
        "low": "can indicate an underactive thyroid",
        "high": "can indicate an overactive thyroid",
    },
    "vitamin_d": {
        "low": "is common and can affect bone health, mood, and immune function",
        "high": "is uncommon and usually related to over-supplementation",
    },
    "vitamin_b12": {
        "low": "can cause fatigue, numbness/tingling, and needs supplementation if confirmed",
        "high": "is usually not a concern and often relates to supplementation",
    },
    "iron": {
        "low": "can contribute to anemia and fatigue",
        "high": "in excess can affect the liver and heart over time",
    },
    "ferritin": {
        "low": "usually confirms low iron stores, even before anemia shows up",
        "high": "can be a sign of inflammation, liver issues, or iron overload",
    },
}


def _explain(key: str, direction: str) -> str:
    notes = PLAIN_LANGUAGE_NOTES.get(key, {})
    return notes.get(direction, "is outside the typical reference range and is worth discussing with your doctor")


def _severity_word(value: float, low: float, high: float, direction: str) -> str:
    """Classify how far outside the range a value is, so the summary can say
    'mildly low' vs 'significantly low' instead of treating a value that's
    1% off the same as one that's 50% off."""
    span = high - low
    if span <= 0:
        return direction
    if direction == "low":
        deviation = (low - value) / span
    else:
        deviation = (value - high) / span
    if deviation >= 0.5:
        return f"significantly {direction}"
    if deviation >= 0.15:
        return f"moderately {direction}"
    return f"mildly {direction}"


def build_summary(extracted_values: dict, flags: list, reference_ranges: dict) -> str:
    """Rule-based narrative summary. Turns extracted values and flags into a
    short, plain-language paragraph explaining what was found and, for
    anything abnormal, what it commonly indicates."""
    if not extracted_values:
        return "No recognized lab values could be extracted from this report. Manual review is recommended."

    tested_labels = [reference_ranges.get(k, {}).get("label", k.replace("_", " ").title()) for k in extracted_values]

    if not flags:
        tested_str = ", ".join(tested_labels)
        return f"This report includes {len(tested_labels)} value(s): {tested_str}. All are within normal reference ranges — no concerning findings."

    sentences = []
    for key, value in extracted_values.items():
        ref = reference_ranges.get(key)
        if not ref:
            continue
        label = ref.get("label", key)
        if value < ref["low"]:
            direction = "low"
        elif value > ref["high"]:
            direction = "high"
        else:
            continue
        severity_phrase = _severity_word(value, ref["low"], ref["high"], direction)
        explanation = _explain(key, direction)
        sentences.append(
            f"{label} is {severity_phrase} at {value} {ref['unit']} (normal range {ref['low']}–{ref['high']} {ref['unit']}), which {explanation}."
        )

    normal_count = len(extracted_values) - len(sentences)
    intro = f"This report includes {len(extracted_values)} tested value(s). " + " ".join(sentences)
    if normal_count > 0:
        intro += f" The remaining {normal_count} value(s) are within normal range."
    intro += " We recommend discussing these findings with your doctor."
    return intro


# def summarize_report(report_text: str) -> dict:
#     reference_ranges = _load_reference_ranges()
#     extracted_values = extract_lab_values(report_text)
#     flags = flag_abnormal_values(extracted_values, reference_ranges)
#     summary = build_summary(extracted_values, flags, reference_ranges)

#     return {"summary": summary, "flags": flags, "extracted_values": extracted_values}


def summarize_report(report_text: str) -> dict:
    reference_ranges = _load_reference_ranges()
    extracted_values = extract_lab_values(report_text)

    print("Reference keys:", reference_ranges.keys())
    print("Extracted values:", extracted_values)

    flags = flag_abnormal_values(extracted_values, reference_ranges)
    print("Flags:", flags)

    summary = build_summary(extracted_values, flags, reference_ranges)

    return {
        "summary": summary,
        "flags": flags,
        "extracted_values": extracted_values,
    }


if __name__ == "__main__":
    sample = """Hemoglobin
Cyanide free
9.8
gm/dl
12.0-15.0
WBC Count
11500
/cumm
4000-11000
Platelet Count
410000
/cumm
150000-410000
Fasting Blood Sugar
145
mg/dl
70-100
TSH
8.2
mIU/L
0.4-4.0"""
    print(json.dumps(summarize_report(sample), indent=2))