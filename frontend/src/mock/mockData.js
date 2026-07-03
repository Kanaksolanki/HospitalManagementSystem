// Use this to build/demo the UI before real backend endpoints are wired in.
// Shapes match API_CONTRACT.md so swapping to real API calls later is a
// find-and-replace, not a rewrite.

export const mockUsers = [
  { id: 1, email: "riya.patient@demo.com", password: "demo123", name: "Riya Kapoor", role: "patient", displayId: "PID000145" },
  { id: 2, email: "sharma.doctor@demo.com", password: "demo123", name: "Dr. Sharma", role: "doctor", displayId: "DOC0012" },
];

export const mockDoctors = [
  { id: 1, doctor_id: "DOC0012", name: "Dr. Sharma", specialization: "Cardiologist", rating: 4.8, visiting_hours: "9:00 AM – 2:00 PM", available_days: ["Mon", "Wed", "Fri"] },
  { id: 2, doctor_id: "DOC0013", name: "Dr. Verma", specialization: "Dermatologist", rating: 4.5, visiting_hours: "11:00 AM – 4:00 PM", available_days: ["Tue", "Thu"] },
  { id: 3, doctor_id: "DOC0014", name: "Dr. Iyer", specialization: "General Physician", rating: 4.6, visiting_hours: "9:00 AM – 1:00 PM", available_days: ["Mon", "Tue", "Wed", "Thu", "Fri"] },
  { id: 4, doctor_id: "DOC0015", name: "Dr. Nair", specialization: "Orthopedic", rating: 4.7, visiting_hours: "2:00 PM – 6:00 PM", available_days: ["Mon", "Thu"] },
];

export const mockSlots = ["9:00 AM", "9:30 AM", "10:00 AM", "11:00 AM", "2:00 PM", "2:30 PM"];

export const mockAppointments = [
  { id: 1, doctor_name: "Dr. Sharma", specialization: "Cardiologist", date: "2026-07-10", time: "10:00 AM", status: "upcoming", reason: "General checkup" },
  { id: 2, doctor_name: "Dr. Iyer", specialization: "General Physician", date: "2026-06-18", time: "9:30 AM", status: "completed", reason: "Fever and fatigue" },
];

export const mockReports = [
  { id: 1, report_type: "Blood Test (CBC)", date: "2026-06-20", hospital: "City Care Hospital", ai_summary: "Hemoglobin slightly low. Platelets and blood sugar normal. Consult physician for mild anemia.", flags: ["Low Hemoglobin"] },
  { id: 2, report_type: "ECG", date: "2026-05-02", hospital: "City Care Hospital", ai_summary: "No abnormalities detected. Heart rhythm within normal range.", flags: [] },
];

export const mockPrescriptions = [
  { id: 1, doctor_name: "Dr. Sharma", date: "2026-06-20", medicines: [{ name: "Ferrous Sulfate", dosage: "325mg", frequency: "Once daily" }], notes: "Take after food. Increase iron-rich foods.", followup_date: "2026-07-20" },
  { id: 2, doctor_name: "Dr. Iyer", date: "2026-06-18", medicines: [{ name: "Paracetamol", dosage: "500mg", frequency: "Twice daily" }, { name: "Cetirizine", dosage: "10mg", frequency: "Once at night" }], notes: "Rest and hydration advised.", followup_date: null },
];

// Doctor-side: patients a doctor can look up
export const mockPatients = [
  {
    patient_id: "PID000145",
    name: "Riya Kapoor",
    age: 24,
    gender: "Female",
    blood_group: "O+",
    allergies: "Penicillin",
    emergency_contact: "+91 98765 43210",
    reports: mockReports,
    prescriptions: mockPrescriptions,
    past_diseases: ["Mild Anemia (2026)"],
  },
  {
    patient_id: "PID000098",
    name: "Arjun Mehta",
    age: 38,
    gender: "Male",
    blood_group: "B+",
    allergies: "None known",
    emergency_contact: "+91 91234 56789",
    reports: [{ id: 3, report_type: "Lipid Profile", date: "2026-04-11", hospital: "City Care Hospital", ai_summary: "LDL cholesterol slightly elevated. Recommend dietary changes and follow-up in 3 months.", flags: ["High LDL"] }],
    prescriptions: [{ id: 3, doctor_name: "Dr. Sharma", date: "2026-04-11", medicines: [{ name: "Atorvastatin", dosage: "10mg", frequency: "Once at night" }], notes: "Low-fat diet recommended.", followup_date: "2026-07-11" }],
    past_diseases: ["Borderline High Cholesterol (2026)"],
  },
];

export const mockQueue = [
  { patient_id: "PID000145", name: "Riya Kapoor", time: "9:00 AM", status: "waiting", reason: "General checkup" },
  { patient_id: "PID000098", name: "Arjun Mehta", time: "9:30 AM", status: "waiting", reason: "Follow-up: cholesterol" },
  { patient_id: "PID000210", name: "Sana Sheikh", time: "10:00 AM", status: "completed", reason: "Fever" },
];

// Used by the drug interaction checker demo on the prescription form
export const knownInteractions = [
  { a: "aspirin", b: "warfarin", severity: "high", note: "Increased bleeding risk" },
  { a: "ibuprofen", b: "warfarin", severity: "high", note: "Increased bleeding risk" },
  { a: "metformin", b: "alcohol", severity: "medium", note: "Risk of lactic acidosis" },
];