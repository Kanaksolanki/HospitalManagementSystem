import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { mockPatients, knownInteractions } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";

function checkInteractions(medicineNames) {
  // TODO: replace with a call through the backend to
  // ai-module/drug_interaction_checker.py's check_drug_interaction()
  const names = medicineNames.map((n) => n.toLowerCase());
  for (let i = 0; i < names.length; i++) {
    for (let j = i + 1; j < names.length; j++) {
      const hit = knownInteractions.find(
        (k) => (k.a === names[i] && k.b === names[j]) || (k.a === names[j] && k.b === names[i])
      );
      if (hit) return hit;
    }
  }
  return null;
}

export default function WritePrescription() {
  const { patientId } = useParams();
  const navigate = useNavigate();
  const patient = mockPatients.find((p) => p.patient_id === patientId);

  const [medicines, setMedicines] = useState([{ name: "", dosage: "", frequency: "" }]);
  const [notes, setNotes] = useState("");
  const [followup, setFollowup] = useState("");
  const [saved, setSaved] = useState(false);

  const interaction = checkInteractions(medicines.map((m) => m.name).filter(Boolean));

  const updateMedicine = (i, field, value) => {
    const next = [...medicines];
    next[i][field] = value;
    setMedicines(next);
  };

  const addMedicine = () => setMedicines([...medicines, { name: "", dosage: "", frequency: "" }]);
  const removeMedicine = (i) => setMedicines(medicines.filter((_, idx) => idx !== i));

  const handleSave = (e) => {
    e.preventDefault();
    // TODO: replace with doctorApi.writePrescription({ patient_id, medicines, notes, followup_date })
    setSaved(true);
  };

  if (!patient) return <div className="page"><p>Patient not found.</p></div>;

  if (saved) {
    return (
      <div className="page">
        <div className="card" style={{ maxWidth: 480, margin: "40px auto", textAlign: "center" }}>
          <span className="badge badge-success" style={{ marginBottom: 12 }}>Prescription saved</span>
          <h2>{patient.name}</h2>
          <p>A PDF will be generated and shared with the patient.</p>
          <button className="btn btn-primary btn-block" onClick={() => navigate(`/doctor/history/${patientId}`)}>
            Back to patient history
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Doctor Portal</span>
        <h1>Write prescription</h1>
        <p>{patient.name} · <span className="id-tag">{patient.patient_id}</span> · Allergies: {patient.allergies}</p>
      </div>
      <PulseDivider />

      <form onSubmit={handleSave} className="card" style={{ maxWidth: 600 }}>
        <label style={{ fontSize: 13, fontWeight: 600, color: "var(--ink-soft)" }}>Medicines</label>
        {medicines.map((m, i) => (
          <div key={i} style={{ display: "flex", gap: 8, marginTop: 8, marginBottom: 8 }}>
            <input placeholder="Name" value={m.name} onChange={(e) => updateMedicine(i, "name", e.target.value)}
              style={{ flex: 2, border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "8px 10px" }} />
            <input placeholder="Dosage" value={m.dosage} onChange={(e) => updateMedicine(i, "dosage", e.target.value)}
              style={{ flex: 1, border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "8px 10px" }} />
            <input placeholder="Frequency" value={m.frequency} onChange={(e) => updateMedicine(i, "frequency", e.target.value)}
              style={{ flex: 1, border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "8px 10px" }} />
            {medicines.length > 1 && (
              <button type="button" className="btn btn-ghost" onClick={() => removeMedicine(i)}>✕</button>
            )}
          </div>
        ))}
        <button type="button" className="btn btn-secondary" onClick={addMedicine} style={{ marginBottom: 16 }}>
          + Add medicine
        </button>

        {interaction && (
          <div className="card" style={{ background: "var(--danger-tint)", borderColor: "var(--danger)", marginBottom: 16 }}>
            <strong style={{ color: "var(--danger)" }}>⚠ Interaction detected</strong>
            <p style={{ margin: "4px 0 0", fontSize: 13, color: "var(--ink)" }}>{interaction.note} — avoid this combination.</p>
          </div>
        )}

        <div className="field">
          <label>Advice / notes</label>
          <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} />
        </div>
        <div className="field">
          <label>Follow-up date (optional)</label>
          <input type="date" value={followup} onChange={(e) => setFollowup(e.target.value)} />
        </div>

        <button className="btn btn-primary btn-block" disabled={!!interaction}>
          {interaction ? "Resolve interaction to save" : "Save prescription"}
        </button>
      </form>
    </div>
  );
}
