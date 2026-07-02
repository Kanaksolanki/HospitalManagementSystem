# AI-Powered Hospital Management System — Team Workflow & Architecture

**Team:** Riya (AI/ML) · Kanak (Frontend – React) · Diksha (Backend – Django REST API)

---

## 0. Read This First: Scope Reality Check

Your doc lists **12 AI features** + a huge patient/doctor dashboard. That is a 6+ month production roadmap, not a student project timeline. If you try to build all of it, you will likely finish none of it well — and "half-working hospital OS" looks worse on a resume than "fully working focused product."

**Recommendation: Build in 2 tiers.**

**Tier 1 — MVP (build this fully, working end-to-end):**
- Auth (Patient + Doctor login/signup, JWT, unique IDs)
- Patient: appointment booking, view doctors, upload reports, prescription history
- Doctor: search patient by ID, view history, write prescription
- AI: **Report Summarizer** + **Disease Risk Predictor** + **Drug Interaction Checker**

**Tier 2 — Stretch goals (add if Tier 1 finishes early):**
- Medical Chatbot, OCR Prescription Reader, No-show Predictor, Follow-up Predictor, Emergency QR Card, Health Dashboard charts

This gives you 3 AI features covering 3 different ML modalities (NLP summarization, classification, rule/embedding-based interaction checking) — great for demonstrating range without overbuilding. You can always add more AI features once the core loop works.

---

## 1. Final Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React (Vite) + plain CSS or Tailwind |
| Backend | Django + Django REST Framework |
| Database | PostgreSQL |
| Auth | JWT (djangorestframework-simplejwt) |
| AI Module | Python (FastAPI microservice **or** Django app — see note below) |
| File storage | Local `/media` folder for now (Cloudinary/S3 later if needed) |

**Important architecture decision:** Run the AI module as **Django app functions called internally** (not a separate microservice) for the MVP. A separate FastAPI service adds deployment complexity (2 servers, CORS, auth-passing) that isn't worth it until you actually need to scale. Riya writes Python functions that Diksha's Django views call directly. Simpler to build, simpler to demo, simpler to deploy on Render.

---

## 2. The Most Important Step: Write the API Contract FIRST (Day 1–2)

Before anyone writes real code, all three of you sit together and agree on:
- Every API endpoint (URL, method, request body, response body)
- Every database table's fields
- What format AI functions take as input and return as output

**Why this matters:** Once this contract exists, Kanak can build the entire frontend against **fake/mock data** matching the contract, Diksha builds the real endpoints to match it, and Riya builds AI functions with a known input/output shape — all **simultaneously**, without waiting on each other. This is what removes the "hinderance" (blocking) you're worried about.

### Core API Contract (starting point — refine together)

```
AUTH
POST   /api/auth/register/          -> {name, email, password, role, phone}
POST   /api/auth/login/             -> {email, password} => {access_token, refresh_token, role, user_id}
GET    /api/auth/me/                -> current user profile

PATIENT
GET    /api/patients/<id>/          -> patient profile
GET    /api/doctors/                -> list all doctors (filter by department)
GET    /api/doctors/<id>/slots/     -> available time slots
POST   /api/appointments/           -> book appointment {doctor_id, date, time, reason}
GET    /api/appointments/mine/      -> patient's appointments
POST   /api/reports/upload/         -> upload report file {patient_id, report_type, file}
GET    /api/reports/mine/           -> list of patient's reports
GET    /api/prescriptions/mine/     -> patient's prescription history

DOCTOR
GET    /api/doctors/search/?patient_id=PID000145   -> find patient
GET    /api/patients/<id>/history/  -> full history (reports, prescriptions, past visits)
POST   /api/prescriptions/          -> {patient_id, medicines, notes, followup_date}
GET    /api/appointments/queue/     -> today's appointment queue for logged-in doctor

AI (internal, called by Django views — not directly hit by frontend)
summarize_report(report_text) -> {summary, flags: [...]}
predict_disease_risk(patient_data: dict) -> {disease, risk_percent, risk_level}
check_drug_interaction(medicine_list: list) -> {interaction_found: bool, details: str}
```

Sit together and turn this into a shared doc (Google Doc or a `API_CONTRACT.md` in the repo) **before Day 3**. This one meeting saves weeks of rework.

---

## 3. Database Schema (Diksha builds this, but everyone should understand it)

Based on your doc, here's the refined schema:

```
User (id, name, email, password, role[patient/doctor], phone, created_at)
Patient (patient_id[PID000145], user_id FK, blood_group, dob, gender, address, 
         insurance, allergies, emergency_contact)
Doctor (doctor_id[DOC0012], user_id FK, specialization, experience, 
        qualification, available_days, visiting_hours, is_approved)
Appointment (id, patient_id FK, doctor_id FK, date, time, status, reason)
MedicalReport (id, patient_id FK, report_type, file, uploaded_date, hospital, ai_summary)
Prescription (id, doctor_id FK, patient_id FK, medicines[JSON], notes, followup_date)
```

Use `PID000145` / `DOC0012` style IDs — auto-generate these on signup (e.g. `PID` + zero-padded auto-increment).

---

## 4. Timeline — Who Does What, When (6-week plan)

This is structured so **no one waits idle** for another person.

### Week 1: Setup + Contract
- **All three together:** finalize API contract & DB schema (above)
- **Diksha:** Django project setup, models, migrations, admin panel, JWT auth endpoints
- **Kanak:** React project setup (Vite), routing, login/signup UI, connect to Diksha's real auth endpoints once ready (Day 3-4)
- **Riya:** Research/finalize approach for each AI feature — decide libraries (see Section 6), collect/create sample datasets, no real coding yet

### Week 2: Core Patient + Doctor Flows
- **Diksha:** Appointment booking APIs, doctor listing, report upload API (file storage)
- **Kanak:** Build Patient Dashboard UI (doctor list, booking flow, report upload) using **mock JSON data** matching the contract — don't wait for Diksha to finish
- **Riya:** Build Report Summarizer as a standalone Python function/notebook, test it independently with sample reports

### Week 3: Integration Point 1
- **Kanak + Diksha:** Connect real booking/report APIs to frontend (swap mock data for real calls)
- **Riya:** Hand off `summarize_report()` function to Diksha to wire into `/api/reports/upload/`
- **Diksha:** Wire AI function into report upload flow (summary saved alongside report)

### Week 4: Doctor Side
- **Diksha:** Patient search-by-ID, full history endpoint, prescription creation API
- **Kanak:** Build Doctor Dashboard UI (search patient, view history, write prescription) with mock data first, then connect
- **Riya:** Build Disease Risk Predictor (train on public dataset — e.g. diabetes/heart disease datasets from Kaggle), build Drug Interaction Checker (can start rule-based with a small interaction dataset, no need for deep ML)

### Week 5: Integration Point 2 + Polish
- **All:** Wire risk predictor + drug interaction checker into doctor's prescription flow
- **Diksha:** Error handling, edge cases, deployment prep (Render/Railway)
- **Kanak:** UI polish, loading states, responsive design, error messages
- **Riya:** Model evaluation, write up accuracy/metrics for resume talking points

### Week 6: Testing, Deployment, Docs
- **All:** End-to-end testing together (one person acts as patient, one as doctor, walk through full flow)
- **Diksha:** Deploy backend + DB (Render + Postgres addon)
- **Kanak:** Deploy frontend (Vercel/Netlify), point to live backend
- **Riya:** Write AI methodology section for README/resume
- **All:** README, demo video, resume bullet points

---

## 5. How to Avoid Blocking Each Other (the actual "workflow" you asked for)

1. **Mock data is your best friend.** Kanak should never wait for a real API — build a `mockData.js` file matching the exact shape from the API contract, build the whole UI against it, then do a 30-minute "swap" session with Diksha once the real endpoint is ready.
2. **Riya builds AI functions in isolation first** (a Jupyter notebook or standalone script with sample input/output), completely decoupled from Django. Only at integration points does she hand off a clean function to Diksha.
3. **Daily 10-minute standup** (even over WhatsApp voice note): what I did, what I'm doing next, what's blocking me.
4. **One shared repo, feature branches.** `git checkout -b feature/patient-dashboard`, `feature/auth`, `feature/risk-predictor`. Merge to `main` only when working. Avoid all three pushing to `main` directly — that's where most "it worked on my machine" pain comes from.
5. **Integration points are scheduled, not accidental** — Weeks 3 and 5 above are explicitly for wiring pieces together, so nobody's surprised mid-week.

---

## 6. AI Feature Notes (for Riya)

| Feature | Approach | Notes |
|---|---|---|
| Report Summarizer | Rule-based extraction (regex for lab values) + template sentences, OR a small pretrained summarization model (e.g. `facebook/bart-large-cnn` via HuggingFace) if you want real NLP | Rule-based is faster to build and more reliable for structured lab reports; pure LLM summarization can hallucinate values — risky for medical data |
| Disease Risk Predictor | Random Forest / XGBoost on public datasets (Pima Diabetes, UCI Heart Disease) | Clean classification project, easy to explain in interviews |
| Drug Interaction Checker | Start rule-based: a CSV of known dangerous combinations (there are public open datasets), simple lookup | Don't over-engineer this with ML — a lookup table is honest and safe. You can mention "designed to be swapped for a trained model with more data" as future work |

Additional AI feature suggestions (pick 1 if Tier 1 finishes early):
- **Appointment No-show Predictor** — logistic regression on patient's past appointment history (attended vs missed), a good lightweight second classification project
- **Symptom-based Doctor Recommender** — patient types symptoms, simple keyword/embedding match to relevant specialization (nice NLP addition, simpler than a full chatbot)

---

## 7. Additional Doctor-Side Features (beyond what you listed)

- **Quick vitals entry** during consultation (BP, sugar, weight) — feeds directly into the risk predictor, closes the loop nicely
- **Prescription templates** — doctor saves common prescriptions (e.g. "standard fever protocol") to reuse
- **Patient notes (private)** — doctor's own notes not visible to patient, useful for continuity of care
- **Referral to another doctor** — generates a referral note, patient can book with the referred doctor directly

---

## 8. Folder Structure for VS Code

Use **one repo with three top-level folders** — simplest for a 3-person team to manage.

```
hospital-management-system/
│
├── README.md
├── API_CONTRACT.md
├── .gitignore
│
├── backend/                        (Diksha)
│   ├── manage.py
│   ├── requirements.txt
│   ├── hms_backend/                # Django project config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── accounts/                   # auth app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── patients/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── doctors/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── appointments/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── reports/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── prescriptions/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── media/                      # uploaded files (reports, etc.)
│
├── ai-module/                      (Riya — built standalone, imported by backend)
│   ├── requirements.txt
│   ├── notebooks/                  # experimentation, model training
│   │   ├── risk_predictor.ipynb
│   │   └── report_summarizer.ipynb
│   ├── models/                     # saved trained models (.pkl, .joblib)
│   │   └── disease_risk_model.pkl
│   ├── report_summarizer.py        # clean callable function
│   ├── risk_predictor.py           # clean callable function
│   ├── drug_interaction_checker.py
│   ├── data/                       # datasets used for training
│   │   └── drug_interactions.csv
│   └── utils/
│       └── preprocessing.py
│
└── frontend/                       (Kanak)
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── public/
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api/
        │   ├── axiosClient.js      # base API setup
        │   ├── authApi.js
        │   ├── patientApi.js
        │   └── doctorApi.js
        ├── mock/
        │   └── mockData.js         # for building UI before real APIs exist
        ├── context/
        │   └── AuthContext.jsx
        ├── components/
        │   ├── layout/
        │   ├── common/
        │   └── forms/
        ├── pages/
        │   ├── Login.jsx
        │   ├── Signup.jsx
        │   ├── patient/
        │   │   ├── PatientDashboard.jsx
        │   │   ├── BookAppointment.jsx
        │   │   ├── UploadReport.jsx
        │   │   └── PrescriptionHistory.jsx
        │   └── doctor/
        │       ├── DoctorDashboard.jsx
        │       ├── PatientSearch.jsx
        │       ├── PatientHistory.jsx
        │       └── WritePrescription.jsx
        ├── hooks/
        └── styles/
```

**Key point on `ai-module/`:** Riya writes clean Python functions here with a stable input/output signature (per the API contract). Diksha imports these directly into Django views — e.g. `from ai_module.risk_predictor import predict_disease_risk`. Keep the `ai-module` folder importable as a plain Python package with no Django dependency inside it — that keeps Riya's work testable on its own.

---

## 9. Immediate Next Steps

1. All three sit together and finalize Section 2 (API contract) — this unblocks everyone
2. Create the GitHub repo with the folder structure above, each person pushes an empty scaffold in their folder
3. Set up branch protection on `main` (optional but good practice) — merge via PR so everyone reviews
4. Start Week 1 tasks

If any of you get stuck at an integration point (e.g. Kanak needs to know exactly what JSON shape Diksha's endpoint returns), that's the moment to come back and ask me — I can help debug the specific handoff.
