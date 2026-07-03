import { Link } from "react-router-dom";
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
        <h1>Good day, {user?.name}</h1>
        <p>{waitingCount} patients waiting today.</p>
      </div>
      <PulseDivider active />

      <div className="grid grid-2" style={{ marginBottom: 24 }}>
        <Link to="/doctor/search" className="card card-hover">
          <h3>Search patient</h3>
          <p>Look up by patient ID or phone number.</p>
        </Link>
        <div className="card">
          <span className="eyebrow">Your ID</span>
          <h3 className="id-tag" style={{ display: "inline-block", fontSize: 15 }}>{user?.displayId}</h3>
        </div>
      </div>

      <h2>Today's queue</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 12 }}>
        {mockQueue.map((q, i) => (
          <div key={i} className="card" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h3 style={{ marginBottom: 2 }}>{q.name}</h3>
              <span className="id-tag">{q.patient_id}</span>
              <span style={{ fontSize: 13, color: "var(--ink-soft)", marginLeft: 10 }}>{q.reason}</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{q.time}</span>
              <Badge variant={STATUS_VARIANT[q.status]}>{q.status}</Badge>
              {q.status === "waiting" && (
                <Link to={`/doctor/history/${q.patient_id}`} className="btn btn-secondary">View</Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}