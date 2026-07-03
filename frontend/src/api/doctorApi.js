import axiosClient from "./axiosClient";

export const searchPatient = (patientId) =>
  axiosClient.get(`/doctors/search/`, { params: { patient_id: patientId } });
export const getPatientHistory = (patientId) =>
  axiosClient.get(`/patients/${patientId}/history/`);
export const writePrescription = (data) => axiosClient.post("/prescriptions/", data);
export const getAppointmentQueue = () => axiosClient.get("/appointments/queue/");