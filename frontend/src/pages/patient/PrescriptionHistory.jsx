import { mockPrescriptions } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";
import EmptyState from "../../components/common/EmptyState";

export default function PrescriptionHistory() {
  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Prescription history</h1>
      </div>
      <PulseDivider />

      {mockPrescriptions.length === 0 ? (
        <EmptyState title="No prescriptions yet" message="Prescriptions from your visits will appear here." />
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {mockPrescriptions.map((p) => (
            <div key={p.id} className="card">
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <h3>{p.doctor_name}</h3>
                <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{p.date}</span>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, margin: "10px 0" }}>
                {p.medicines.map((m, i) => (
                  <span key={i} className="badge badge-primary">
                    {m.name} · {m.dosage} · {m.frequency}
                  </span>
                ))}
              </div>
              <p style={{ fontSize: 13 }}>{p.notes}</p>
              {p.followup_date && (
                <p style={{ fontSize: 13, fontWeight: 600, color: "var(--ink)" }}>
                  Follow-up: {p.followup_date}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}