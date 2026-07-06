# API Contract (v1 — edit together, keep updated as source of truth)

## AUTH
- `POST /api/auth/register/` -> `{name, email, password, role, phone}`
- `POST /api/auth/login/` -> `{email, password}` => `{access_token, refresh_token, role, user_id}`
- `GET /api/auth/me/` -> current user profile

## PATIENT
- `GET /api/patients/<id>/` -> patient profile
- `GET /api/doctors/` -> list all doctors (filter by department)
- `GET /api/doctors/<id>/slots/` -> available time slots
- `POST /api/appointments/` -> book appointment `{doctor_id, date, time, reason}`
- `GET /api/appointments/mine/` -> patient's appointments
- `POST /api/reports/upload/` -> upload report file `{patient_id, report_type, file}`
- `GET /api/reports/mine/` -> list of patient's reports
- `GET /api/prescriptions/mine/` -> patient's prescription history

## DOCTOR
- `GET /api/doctors/search/?patient_id=PID000145` -> find patient
- `GET /api/patients/<id>/history/` -> full history (reports, prescriptions, past visits)
- `POST /api/prescriptions/` -> `{patient_id, medicines, notes, followup_date}`
- `GET /api/appointments/queue/` -> today's appointment queue for logged-in doctor

## AI (internal — called by Django views, not hit directly by frontend)
- `summarize_report(report_text: str) -> {summary: str, flags: list, extracted_values: dict}`
  - Hybrid: regex extraction of lab values (vs. `ai-module/data/lab_reference_ranges.json`) + Claude API narrative.
  - `extracted_values` is additive beyond the original contract — safe to ignore if unused.
- `predict_disease_risk(patient_data: dict) -> {disease: str, risk_percent: float, risk_level: str}`
- `check_drug_interaction(medicine_list: list) -> {interaction_found: bool, details: str}`
- `summarize_patient_history(patient_history: dict) -> {summary: str, key_points: list, flags: list}`
  - New: used on the doctor's patient-history view during consultation (`GET /api/patients/<id>/history/`).
  - Input shape: `{patient_id, name, age, gender, allergies, past_diseases, reports: [...], prescriptions: [...], appointments: [...]}`
  - Hybrid: rule-based extraction of allergies/active meds/chronic conditions/report flags + Claude API narrative handoff note.
  - `key_points` is always rule-based (safe to render even if the Claude call fails); `summary` falls back to a plain-text version built from the same facts if the API is unavailable.

---
Update this file whenever an endpoint's shape changes. Whoever changes it should
message the other two — this file is the thing that keeps all three of you unblocked.
