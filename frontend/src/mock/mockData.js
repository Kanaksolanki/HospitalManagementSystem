// Use this to build UI before real backend endpoints are ready.
// Shape should match API_CONTRACT.md exactly so swapping to real data is a one-line change.

export const mockDoctors = [
  { id: 1, doctor_id: "DOC0012", name: "Dr. Sharma", specialization: "Cardiologist", rating: 4.8, visiting_hours: "9AM-2PM" },
  { id: 2, doctor_id: "DOC0013", name: "Dr. Verma", specialization: "Dermatologist", rating: 4.5, visiting_hours: "11AM-4PM" },
];

export const mockAppointments = [
  { id: 1, doctor_name: "Dr. Sharma", date: "2026-07-10", time: "10:00", status: "upcoming", reason: "General checkup" },
];

export const mockReports = [
  { id: 1, report_type: "Blood Test", date: "2026-06-20", ai_summary: "Hemoglobin slightly low. Consult physician for mild anemia." },
];

export const mockPrescriptions = [
  { id: 1, doctor_name: "Dr. Sharma", medicines: [{ name: "Paracetamol", dosage: "500mg", frequency: "Twice daily" }], notes: "Take after food", followup_date: "2026-07-20" },
];
