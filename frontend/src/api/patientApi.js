import axiosClient from "./axiosClient";

export const getDoctors = () => axiosClient.get("/doctors/");
export const getDoctorSlots = (doctorId) => axiosClient.get(`/doctors/${doctorId}/slots/`);
export const bookAppointment = (data) => axiosClient.post("/appointments/", data);
export const getMyAppointments = () => axiosClient.get("/appointments/mine/");
export const uploadReport = (formData) =>
  axiosClient.post("/reports/upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const getMyReports = () => axiosClient.get("/reports/mine/");
export const getMyPrescriptions = () => axiosClient.get("/prescriptions/mine/");
