"""
Patient Chatbot
Answers general health questions AND questions about the patient's own
records (appointments, prescriptions, reports), using Claude with the
patient's context injected into the prompt.

Input:  message (str), patient_context (dict) - e.g.
        {"name": "...", "upcoming_appointments": [...], "recent_prescriptions": [...],
         "recent_reports": [...]}
Output: {"reply": str}

If no ANTHROPIC_API_KEY is set, returns a safe fallback message instead of
crashing -- same pattern as report_summarizer.py and patient_history_summarizer.py.
"""

import json
from utils.grok_client import get_narrative

SYSTEM_PROMPT = """You are a helpful assistant inside a hospital management app.
You can answer general health questions AND questions about the patient's own
appointments, prescriptions, and reports, using the context provided.

Rules:
- You are NOT a doctor. For anything serious (symptoms that sound urgent,
  medication changes, diagnosis questions), tell the patient to consult their
  doctor rather than answering directly.
- Keep answers short and clear, 2-4 sentences unless the question needs more.
- When asked about their own data (appointments, prescriptions, reports),
  answer only from the context given -- never invent dates, medicines, or
  results that aren't in the context.
"""

FALLBACK_REPLY = (
    "I'm currently unable to reach the AI service. For questions about your "
    "appointments, prescriptions, or reports, please check your dashboard, "
    "or contact your doctor directly for medical concerns."
)


def get_chat_response(message: str, patient_context: dict) -> dict:
    context_str = json.dumps(patient_context, indent=2, default=str)
    user_prompt = f"Patient context:\n{context_str}\n\nPatient's question:\n{message}"

    reply = get_narrative(SYSTEM_PROMPT, user_prompt, max_tokens=400)
    if reply is None:
        reply = FALLBACK_REPLY

    return {"reply": reply}


if __name__ == "__main__":
    sample_context = {
        "name": "Riya Kapoor",
        "upcoming_appointments": [{"doctor": "Dr. Mehta", "date": "2026-07-20"}],
        "recent_prescriptions": [{"medicines": ["Ferrous Sulfate"], "date": "2026-07-01"}],
        "recent_reports": [],
    }
    print(get_chat_response("When is my next appointment?", sample_context))
    print(get_chat_response("I've had a headache for 3 days, what should I do?", sample_context))