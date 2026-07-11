// import { Link } from "react-router-dom";
// import { useAuth } from "../../context/AuthContext";
// import PulseDivider from "../../components/common/PulseDivider";
// import Badge from "../../components/common/Badge";
// import { mockQueue } from "../../mock/mockData";

// const STATUS_VARIANT = { waiting: "accent", completed: "success", cancelled: "danger" };

// export default function DoctorDashboard() {
//   const { user } = useAuth();
//   const waitingCount = mockQueue.filter((q) => q.status === "waiting").length;

//   return (
//     <div className="page">
//       <div className="page-header">
//         <span className="eyebrow">Doctor Portal</span>
//         <h1>Good day, {user?.name}</h1>
//         <p>{waitingCount} patients waiting today.</p>
//       </div>
//       <PulseDivider active />

//       <div className="grid grid-2" style={{ marginBottom: 24 }}>
//         <Link to="/doctor/search" className="card card-hover">
//           <h3>Search patient</h3>
//           <p>Look up by patient ID or phone number.</p>
//         </Link>
//         <div className="card">
//           <span className="eyebrow">Your ID</span>
//           <h3 className="id-tag" style={{ display: "inline-block", fontSize: 15 }}>{user?.displayId}</h3>
//         </div>
//       </div>

//       <h2>Today's queue</h2>
//       <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 12 }}>
//         {mockQueue.map((q, i) => (
//           <div key={i} className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
//             <div>
//               <h3 style={{ marginBottom: 2 }}>{q.name}</h3>
//               <span className="id-tag">{q.patient_id}</span>
//               <span style={{ fontSize: 13, color: "var(--ink-soft)", marginLeft: 10 }}>{q.reason}</span>
//             </div>
//             <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
//               <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{q.time}</span>
//               <Badge variant={STATUS_VARIANT[q.status]}>{q.status}</Badge>
//               {q.status === "waiting" && (
//                 <Link to={`/doctor/history/${q.patient_id}`} className="btn btn-secondary">View</Link>
//               )}
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }


import { Link } from "react-router-dom";
import { Users, Search, CreditCard } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import PulseDivider from "../../components/common/PulseDivider";
import Badge from "../../components/common/Badge";
import { mockQueue } from "../../mock/mockData";

const STATUS_VARIANT = { waiting: "accent", completed: "success", cancelled: "danger" };

export default function DoctorDashboard() {
  const { user } = useAuth();
  const waitingCount = mockQueue.filter((q) => q.status === "waiting").length;

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Doctor Portal</span>
        <h1>Good day, {user?.name?.replace("Dr. ", "")}.</h1>
        <p>Today's queue at a glance.</p>
      </div>
      <PulseDivider active />

      <div className="grid grid-3" style={{ marginBottom: 28 }}>
        <div className="card">
          <span className="card-label"><Users size={14} /> Waiting today</span>
          <h1 style={{ marginTop: 10, marginBottom: 4 }}>{waitingCount}</h1>
          <p style={{ margin: 0 }}>of {mockQueue.length} scheduled</p>
        </div>

        <Link to="/doctor/search" className="card card-hover">
          <span className="card-label"><Search size={14} /> Find a patient</span>
          <p style={{ margin: "10px 0 0", color: "var(--ink)" }}>Search by patient ID or name to open their full history.</p>
          <span className="card-link" style={{ display: "inline-block", marginTop: 8 }}>Open search →</span>
        </Link>

        <div className="card">
          <span className="card-label"><CreditCard size={14} /> Your Doctor ID</span>
          <h3 className="id-tag" style={{ display: "inline-block", fontSize: 16, marginTop: 8 }}>{user?.displayId}</h3>
          <p style={{ marginTop: 8 }}>{user?.specialization} · Rating {user?.rating}</p>
        </div>
      </div>

      <h2>Today's queue</h2>
      <div className="table-wrap" style={{ marginTop: 12 }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Patient</th>
              <th>ID</th>
              <th>Reason</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {mockQueue.map((q, i) => (
              <tr key={i}>
                <td>{q.time}</td>
                <td style={{ fontWeight: 600 }}>{q.name}</td>
                <td><span className="id-tag">{q.patient_id}</span></td>
                <td>{q.reason}</td>
                <td><Badge variant={STATUS_VARIANT[q.status]}>{q.status}</Badge></td>
                <td style={{ textAlign: "right" }}>
                  <Link to={`/doctor/history/${q.patient_id}`} className="card-link">Open history →</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}