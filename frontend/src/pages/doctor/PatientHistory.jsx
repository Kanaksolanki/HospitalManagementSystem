import { useParams, Link } from "react-router-dom";
import { mockPatients } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";
import Badge from "../../components/common/Badge";
import EmptyState from "../../components/common/EmptyState";

export default function PatientHistory() {
  const { patientId } = useParams();
  const patient = mockPatients.find((p) => p.patient_id === patientId);

  if (!patient) {
    return (
      <div className="page">
        <EmptyState title="Patient not found" message={`No record for ${patientId}.`} />
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
        <div>
          <span className="eyebrow">Doctor Portal</span>
          <h1>{patient.name}</h1>
          <span className="id-tag">{patient.patient_id}</span>
          <span style={{ fontSize: 13, color: "var(--ink-soft)", marginLeft: 10 }}>
            {patient.age} yrs · {patient.gender} · {patient.blood_group}
          </span>
        </div>
        <Link to={`/doctor/prescribe/${patient.patient_id}`} className="btn btn-primary">
          Write prescription
        </Link>
      </div>
      <PulseDivider />

      <div className="grid grid-2" style={{ marginBottom: 24 }}>
        <div className="card">
          <span className="eyebrow">Allergies</span>
          <p style={{ margin: 0, color: "var(--ink)" }}>{patient.allergies}</p>
        </div>
        <div className="card">
          <span className="eyebrow">Emergency contact</span>
          <p style={{ margin: 0, color: "var(--ink)" }}>{patient.emergency_contact}</p>
        </div>
      </div>

      <h2>Past conditions</h2>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", margin: "10px 0 24px" }}>
        {patient.past_diseases.map((d, i) => <Badge key={i} variant="accent">{d}</Badge>)}
      </div>

      <h2>Reports</h2>
      <div className="grid grid-2" style={{ margin: "10px 0 24px" }}>
        {patient.reports.map((r) => (
          <div key={r.id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <h3>{r.report_type}</h3>
              {r.flags.length > 0 ? <Badge variant="accent">{r.flags[0]}</Badge> : <Badge variant="success">Clear</Badge>}
            </div>
            <p style={{ margin: "4px 0" }}>{r.date}</p>
            <p style={{ fontSize: 13 }}>{r.ai_summary}</p>
          </div>
        ))}
      </div>

      <h2>Previous prescriptions</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 10 }}>
        {patient.prescriptions.map((p) => (
          <div key={p.id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <h3>{p.doctor_name}</h3>
              <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{p.date}</span>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, margin: "8px 0" }}>
              {p.medicines.map((m, i) => (
                <span key={i} className="badge badge-primary">{m.name} · {m.dosage}</span>
              ))}
            </div>
            <p style={{ fontSize: 13 }}>{p.notes}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
