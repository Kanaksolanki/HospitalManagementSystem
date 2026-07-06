// Use this to build/demo the UI before real backend endpoints are wired in.
// Shapes match API_CONTRACT.md so swapping to real API calls later is a
// find-and-replace, not a rewrite.

export const mockUsers = [
  { id: 1, email: "riya.patient@demo.com", password: "demo123", name: "Riya Kapoor", role: "patient", displayId: "PID000145" },
  { id: 2, email: "sharma.doctor@demo.com", password: "demo123", name: "Dr. Sharma", role: "doctor", displayId: "DOC0012" },
];

export const mockDoctors = [
  // Cardiologist
  { id: 1, doctor_id: "DOC0012", name: "Dr. Sharma", specialization: "Cardiologist", rating: 4.8, visiting_hours: "9:00 AM – 2:00 PM", available_days: ["Mon", "Wed", "Fri"] },
  { id: 2, doctor_id: "DOC0024", name: "Dr. Kulkarni", specialization: "Cardiologist", rating: 4.6, visiting_hours: "3:00 PM – 6:00 PM", available_days: ["Tue", "Thu"] },

  // Dermatologist
  { id: 3, doctor_id: "DOC0013", name: "Dr. Verma", specialization: "Dermatologist", rating: 4.5, visiting_hours: "11:00 AM – 4:00 PM", available_days: ["Tue", "Thu"] },
  { id: 4, doctor_id: "DOC0025", name: "Dr. Chatterjee", specialization: "Dermatologist", rating: 4.7, visiting_hours: "10:00 AM – 1:00 PM", available_days: ["Mon", "Wed", "Fri"] },

  // General Physician
  { id: 5, doctor_id: "DOC0014", name: "Dr. Iyer", specialization: "General Physician", rating: 4.6, visiting_hours: "9:00 AM – 1:00 PM", available_days: ["Mon", "Tue", "Wed", "Thu", "Fri"] },
  { id: 6, doctor_id: "DOC0026", name: "Dr. Pillai", specialization: "General Physician", rating: 4.5, visiting_hours: "2:00 PM – 6:00 PM", available_days: ["Mon", "Tue", "Wed", "Thu", "Fri"] },
  { id: 7, doctor_id: "DOC0027", name: "Dr. Agarwal", specialization: "General Physician", rating: 4.8, visiting_hours: "8:00 AM – 12:00 PM", available_days: ["Sat"] },

  // Orthopedic
  { id: 8, doctor_id: "DOC0015", name: "Dr. Nair", specialization: "Orthopedic", rating: 4.7, visiting_hours: "2:00 PM – 6:00 PM", available_days: ["Mon", "Thu"] },
  { id: 9, doctor_id: "DOC0028", name: "Dr. Deshmukh", specialization: "Orthopedic", rating: 4.4, visiting_hours: "9:00 AM – 12:00 PM", available_days: ["Wed", "Fri"] },

  // Pediatrician
  { id: 10, doctor_id: "DOC0016", name: "Dr. Khan", specialization: "Pediatrician", rating: 4.9, visiting_hours: "10:00 AM – 3:00 PM", available_days: ["Mon", "Wed", "Fri"] },
  { id: 11, doctor_id: "DOC0029", name: "Dr. Sinha", specialization: "Pediatrician", rating: 4.6, visiting_hours: "1:00 PM – 5:00 PM", available_days: ["Tue", "Thu"] },

  // Neurologist
  { id: 12, doctor_id: "DOC0017", name: "Dr. Reddy", specialization: "Neurologist", rating: 4.7, visiting_hours: "1:00 PM – 5:00 PM", available_days: ["Tue", "Thu"] },
  { id: 13, doctor_id: "DOC0030", name: "Dr. Bose", specialization: "Neurologist", rating: 4.5, visiting_hours: "9:00 AM – 12:00 PM", available_days: ["Mon", "Fri"] },

  // Gynecologist
  { id: 14, doctor_id: "DOC0018", name: "Dr. Gupta", specialization: "Gynecologist", rating: 4.8, visiting_hours: "9:00 AM – 12:00 PM", available_days: ["Mon", "Wed", "Fri"] },
  { id: 15, doctor_id: "DOC0031", name: "Dr. Krishnan", specialization: "Gynecologist", rating: 4.6, visiting_hours: "2:00 PM – 5:00 PM", available_days: ["Tue", "Thu"] },

  // ENT Specialist
  { id: 16, doctor_id: "DOC0019", name: "Dr. Bhatt", specialization: "ENT Specialist", rating: 4.4, visiting_hours: "3:00 PM – 6:00 PM", available_days: ["Tue", "Thu", "Sat"] },
  { id: 17, doctor_id: "DOC0032", name: "Dr. Shetty", specialization: "ENT Specialist", rating: 4.6, visiting_hours: "9:00 AM – 1:00 PM", available_days: ["Mon", "Wed"] },

  // Psychiatrist
  { id: 18, doctor_id: "DOC0020", name: "Dr. Malhotra", specialization: "Psychiatrist", rating: 4.6, visiting_hours: "11:00 AM – 2:00 PM", available_days: ["Wed", "Fri"] },
  { id: 19, doctor_id: "DOC0033", name: "Dr. Choudhury", specialization: "Psychiatrist", rating: 4.7, visiting_hours: "3:00 PM – 6:00 PM", available_days: ["Mon", "Thu"] },

  // Dentist
  { id: 20, doctor_id: "DOC0021", name: "Dr. Joshi", specialization: "Dentist", rating: 4.5, visiting_hours: "10:00 AM – 4:00 PM", available_days: ["Mon", "Tue", "Wed", "Thu", "Fri"] },
  { id: 21, doctor_id: "DOC0034", name: "Dr. Kapoor", specialization: "Dentist", rating: 4.6, visiting_hours: "9:00 AM – 1:00 PM", available_days: ["Sat"] },

  // Ophthalmologist
  { id: 22, doctor_id: "DOC0022", name: "Dr. Rao", specialization: "Ophthalmologist", rating: 4.7, visiting_hours: "9:00 AM – 1:00 PM", available_days: ["Mon", "Thu", "Sat"] },
  { id: 23, doctor_id: "DOC0035", name: "Dr. Varma", specialization: "Ophthalmologist", rating: 4.5, visiting_hours: "2:00 PM – 5:00 PM", available_days: ["Tue", "Fri"] },

  // Endocrinologist
  { id: 24, doctor_id: "DOC0023", name: "Dr. Menon", specialization: "Endocrinologist", rating: 4.6, visiting_hours: "2:00 PM – 5:00 PM", available_days: ["Tue", "Fri"] },
  { id: 25, doctor_id: "DOC0036", name: "Dr. Trivedi", specialization: "Endocrinologist", rating: 4.4, visiting_hours: "10:00 AM – 1:00 PM", available_days: ["Mon", "Wed"] },
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