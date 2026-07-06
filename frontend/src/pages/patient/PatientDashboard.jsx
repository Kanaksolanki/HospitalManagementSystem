import { Link } from "react-router-dom";
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
        <h1>Hello, {user?.name?.split(" ")[0]}</h1>
        <p>Here's what's happening with your care.</p>
      </div>
      <PulseDivider active />

      <div className="grid grid-3" style={{ marginBottom: 24 }}>
        <div className="card">
          <span className="eyebrow">Next appointment</span>
          {upcoming ? (
            <>
              <h3>{upcoming.doctor_name}</h3>
              <p style={{ margin: "4px 0" }}>{upcoming.specialization}</p>
              <p style={{ margin: 0, color: "var(--ink)", fontWeight: 600 }}>
                {upcoming.date} · {upcoming.time}
              </p>
            </>
          ) : (
            <p>No upcoming appointments.</p>
          )}
        </div>

        <div className="card">
          <span className="eyebrow">Latest report</span>
          {latestReport ? (
            <>
              <h3>{latestReport.report_type}</h3>
              <p style={{ margin: "4px 0 8px" }}>{latestReport.date}</p>
              {latestReport.flags.length > 0 ? (
                <Badge variant="accent">{latestReport.flags[0]}</Badge>
              ) : (
                <Badge variant="success">No flags</Badge>
              )}
            </>
          ) : (
            <p>No reports yet.</p>
          )}
        </div>

        <div className="card">
          <span className="eyebrow">Your ID</span>
          <h3 className="id-tag" style={{ display: "inline-block", fontSize: 15 }}>{user?.displayId}</h3>
          <p style={{ marginTop: 8 }}>Share this with your doctor at check-in.</p>
        </div>
      </div>

      <div className="grid grid-3">
        <Link to="/patient/book" className="card card-hover">
          <h3>Book appointment</h3>
          <p>Find a doctor and reserve a time slot.</p>
        </Link>
        <Link to="/patient/upload-report" className="card card-hover">
          <h3>Upload report</h3>
          <p>Add a lab report or scan for AI summary.</p>
        </Link>
        <Link to="/patient/prescriptions" className="card card-hover">
          <h3>Prescription history</h3>
          <p>View every prescription you've received.</p>
        </Link>
      </div>
    </div>
  );
}
