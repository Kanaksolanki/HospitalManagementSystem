import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import PatientDashboard from "./pages/patient/PatientDashboard.jsx";
import BookAppointment from "./pages/patient/BookAppointment.jsx";
import UploadReport from "./pages/patient/UploadReport.jsx";
import PrescriptionHistory from "./pages/patient/PrescriptionHistory.jsx";
import DoctorDashboard from "./pages/doctor/DoctorDashboard.jsx";
import PatientSearch from "./pages/doctor/PatientSearch.jsx";
import PatientHistory from "./pages/doctor/PatientHistory.jsx";
import WritePrescription from "./pages/doctor/WritePrescription.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route path="/patient" element={<PatientDashboard />} />
      <Route path="/patient/book" element={<BookAppointment />} />
      <Route path="/patient/upload-report" element={<UploadReport />} />
      <Route path="/patient/prescriptions" element={<PrescriptionHistory />} />

      <Route path="/doctor" element={<DoctorDashboard />} />
      <Route path="/doctor/search" element={<PatientSearch />} />
      <Route path="/doctor/history/:patientId" element={<PatientHistory />} />
      <Route path="/doctor/prescribe/:patientId" element={<WritePrescription />} />
    </Routes>
  );
}
