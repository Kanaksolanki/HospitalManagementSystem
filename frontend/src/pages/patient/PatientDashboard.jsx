// import { Link } from "react-router-dom";
// import { useAuth } from "../../context/AuthContext";
// import PulseDivider from "../../components/common/PulseDivider";
// import Badge from "../../components/common/Badge";
// import { mockAppointments, mockPatients } from "../../mock/mockData";

// export default function PatientDashboard() {
//   const { user } = useAuth();
//   const patient = mockPatients.find((p) => p.patient_id === user?.displayId);
//   const upcoming = mockAppointments.find((a) => a.status === "upcoming");
//   const latestReport = patient?.reports?.[0];

//   return (
//     <div className="page">
//       <div className="page-header">
//         <span className="eyebrow">Patient Portal</span>
//         <h1>Hello, {user?.name?.split(" ")[0]}</h1>
//         <p>Here's what's happening with your care.</p>
//       </div>
//       <PulseDivider active />

//       <div className="grid grid-3" style={{ marginBottom: 24 }}>
//         <div className="card">
//           <span className="eyebrow">Next appointment</span>
//           {upcoming ? (
//             <>
//               <h3>{upcoming.doctor_name}</h3>
//               <p style={{ margin: "4px 0" }}>{upcoming.specialization}</p>
//               <p style={{ margin: 0, color: "var(--ink)", fontWeight: 600 }}>
//                 {upcoming.date} · {upcoming.time}
//               </p>
//             </>
//           ) : (
//             <p>No upcoming appointments.</p>
//           )}
//         </div>

//         <div className="card">
//           <span className="eyebrow">Latest report</span>
//           {latestReport ? (
//             <>
//               <h3>{latestReport.report_type}</h3>
//               <p style={{ margin: "4px 0 8px" }}>{latestReport.date}</p>
//               {latestReport.flags.length > 0 ? (
//                 <Badge variant="accent">{latestReport.flags[0]}</Badge>
//               ) : (
//                 <Badge variant="success">No flags</Badge>
//               )}
//             </>
//           ) : (
//             <p>No reports yet.</p>
//           )}
//         </div>

//         <div className="card">
//           <span className="eyebrow">Your ID</span>
//           <h3 className="id-tag" style={{ display: "inline-block", fontSize: 15 }}>{user?.displayId}</h3>
//           <p style={{ marginTop: 8 }}>Share this with your doctor at check-in.</p>
//         </div>
//       </div>

//       <div className="grid grid-3">
//         <Link to="/patient/book" className="card card-hover">
//           <h3>Book appointment</h3>
//           <p>Find a doctor and reserve a time slot.</p>
//         </Link>
//         <Link to="/patient/upload-report" className="card card-hover">
//           <h3>Upload report</h3>
//           <p>Add a lab report or scan for AI summary.</p>
//         </Link>
//         <Link to="/patient/prescriptions" className="card card-hover">
//           <h3>Prescription history</h3>
//           <p>View every prescription you've received.</p>
//         </Link>
//       </div>
//     </div>
//   );
// }


import { Link } from "react-router-dom";
import { CalendarClock, CreditCard, Sparkles, CalendarPlus, FileUp, Pill } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import PulseDivider from "../../components/common/PulseDivider";
import Badge from "../../components/common/Badge";
import { mockAppointments, mockPatients } from "../../mock/mockData";

export default function PatientDashboard() {
  const { user } = useAuth();
  const patient = mockPatients.find((p) => p.patient_id === user?.displayId);
  const upcoming = mockAppointments.find((a) => a.status === "upcoming");
  const latestReport = patient?.reports?.[0];

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Hello, {user?.name?.split(" ")[0]}.</h1>
        <p>Here's a quick look at your upcoming care.</p>
      </div>
      <PulseDivider active />

      <div className="grid grid-2" style={{ marginBottom: 16 }}>
        <div className="card">
          <div className="card-label-row">
            <span className="card-label"><CalendarClock size={14} /> Next appointment</span>
            <Link to="/patient/book" className="card-link">Book new →</Link>
          </div>
          {upcoming ? (
            <>
              <h3>{upcoming.doctor_name}</h3>
              <p style={{ margin: "2px 0 10px" }}>{upcoming.specialization}</p>
              <div style={{ display: "flex", gap: 8 }}>
                <Badge variant="primary">{upcoming.date}</Badge>
                <Badge variant="accent">{upcoming.time}</Badge>
                <Badge variant="neutral">{upcoming.reason}</Badge>
              </div>
            </>
          ) : (
            <p>No upcoming appointments.</p>
          )}
        </div>

        <div className="card">
          <span className="card-label"><CreditCard size={14} /> Your Patient ID</span>
          <h3 className="id-tag" style={{ display: "inline-block", fontSize: 16, marginTop: 8 }}>{user?.displayId}</h3>
          <p style={{ marginTop: 8 }}>
            Blood group {patient?.blood_group} · {patient?.age} yrs · {patient?.gender}
          </p>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-label-row">
          <span className="card-label"><Sparkles size={14} /> Latest report — AI summary</span>
          <Link to="/patient/upload-report" className="card-link">Upload new →</Link>
        </div>
        {latestReport ? (
          <>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
              <h3 style={{ margin: 0 }}>{latestReport.report_type}</h3>
              <span className="id-tag">{latestReport.id}</span>
              <Badge variant="neutral">{latestReport.date}</Badge>
            </div>
            <p style={{ margin: 0 }}>{latestReport.ai_summary}</p>
          </>
        ) : (
          <p>No reports uploaded yet.</p>
        )}
      </div>

      <h2>Quick access</h2>
      <div className="grid grid-3" style={{ marginTop: 12 }}>
        <Link to="/patient/book" className="card card-hover">
          <CalendarPlus size={18} color="var(--primary)" style={{ marginBottom: 8 }} />
          <h3>Book appointment</h3>
          <p>Choose a department, doctor, and slot in 3 steps.</p>
        </Link>
        <Link to="/patient/upload-report" className="card card-hover">
          <FileUp size={18} color="var(--primary)" style={{ marginBottom: 8 }} />
          <h3>Upload report</h3>
          <p>Get an AI summary and flagged findings.</p>
        </Link>
        <Link to="/patient/prescriptions" className="card card-hover">
          <Pill size={18} color="var(--primary)" style={{ marginBottom: 8 }} />
          <h3>Prescriptions</h3>
          <p>View past medicines and follow-up dates.</p>
        </Link>
      </div>
    </div>
  );
}
