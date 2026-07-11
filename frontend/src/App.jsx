// import { Routes, Route, Navigate } from "react-router-dom";
// import { AuthProvider, useAuth } from "./context/AuthContext";
// import Navbar from "./components/layout/Navbar";

// import Login from "./pages/Login.jsx";
// import Signup from "./pages/Signup.jsx";
// import PatientDashboard from "./pages/patient/PatientDashboard.jsx";
// import BookAppointment from "./pages/patient/BookAppointment.jsx";
// import UploadReport from "./pages/patient/UploadReport.jsx";
// import PrescriptionHistory from "./pages/patient/PrescriptionHistory.jsx";
// import DoctorDashboard from "./pages/doctor/DoctorDashboard.jsx";
// import PatientSearch from "./pages/doctor/PatientSearch.jsx";
// import PatientHistory from "./pages/doctor/PatientHistory.jsx";
// import WritePrescription from "./pages/doctor/WritePrescription.jsx";

// function Protected({ role, children }) {
//   const { user } = useAuth();
//   if (!user) return <Navigate to="/" replace />;
//   if (role && user.role !== role) return <Navigate to="/" replace />;
//   return children;
// }

// function Shell() {
//   const { user } = useAuth();
//   return (
//     <>
//       {user && <Navbar />}
//       <Routes>
//         <Route path="/" element={<Login />} />
//         <Route path="/signup" element={<Signup />} />

//         <Route path="/patient" element={<Protected role="patient"><PatientDashboard /></Protected>} />
//         <Route path="/patient/book" element={<Protected role="patient"><BookAppointment /></Protected>} />
//         <Route path="/patient/upload-report" element={<Protected role="patient"><UploadReport /></Protected>} />
//         <Route path="/patient/prescriptions" element={<Protected role="patient"><PrescriptionHistory /></Protected>} />

//         <Route path="/doctor" element={<Protected role="doctor"><DoctorDashboard /></Protected>} />
//         <Route path="/doctor/search" element={<Protected role="doctor"><PatientSearch /></Protected>} />
//         <Route path="/doctor/history/:patientId" element={<Protected role="doctor"><PatientHistory /></Protected>} />
//         <Route path="/doctor/prescribe/:patientId" element={<Protected role="doctor"><WritePrescription /></Protected>} />
//       </Routes>
//     </>
//   );
// }

// export default function App() {
//   return (
//     <AuthProvider>
//       <Shell />
//     </AuthProvider>
//   );
// }

import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Sidebar from "./components/layout/Sidebar";

import Landing from "./pages/Landing.jsx";
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
import Assistant from "./pages/Assistant.jsx";

function Protected({ role, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (role && user.role !== role) return <Navigate to="/login" replace />;
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">{children}</div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/patient" element={<Protected role="patient"><PatientDashboard /></Protected>} />
        <Route path="/patient/book" element={<Protected role="patient"><BookAppointment /></Protected>} />
        <Route path="/patient/upload-report" element={<Protected role="patient"><UploadReport /></Protected>} />
        <Route path="/patient/prescriptions" element={<Protected role="patient"><PrescriptionHistory /></Protected>} />
        <Route path="/patient/assistant" element={<Protected role="patient"><Assistant /></Protected>} />

        <Route path="/doctor" element={<Protected role="doctor"><DoctorDashboard /></Protected>} />
        <Route path="/doctor/search" element={<Protected role="doctor"><PatientSearch /></Protected>} />
        <Route path="/doctor/history/:patientId" element={<Protected role="doctor"><PatientHistory /></Protected>} />
        <Route path="/doctor/prescribe/:patientId" element={<Protected role="doctor"><WritePrescription /></Protected>} />
        <Route path="/doctor/assistant" element={<Protected role="doctor"><Assistant /></Protected>} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}