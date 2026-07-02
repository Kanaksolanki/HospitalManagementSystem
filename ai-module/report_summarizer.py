"""
Report Summarizer
Input:  report_text (str) - raw text extracted from a medical report
Output: {"summary": str, "flags": list[str]}

Start with rule-based extraction (regex for lab values against normal ranges)
before reaching for a full NLP model — safer and easier to explain for medical data.
"""


def summarize_report(report_text: str) -> dict:
    # TODO: implement extraction + summary logic
    summary = "Sample summary — replace with real logic."
    flags = []
    return {"summary": summary, "flags": flags}


if __name__ == "__main__":
    sample = "Hemoglobin: 11.2 g/dL, Platelets: 250000, Blood Sugar: 95 mg/dL"
    print(summarize_report(sample))
