import { useState } from "react";
import { mockDoctors, mockSlots } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";

const DEPARTMENTS = [...new Set(mockDoctors.map((d) => d.specialization))];

export default function BookAppointment() {
  const [step, setStep] = useState(1);
  const [department, setDepartment] = useState(null);
  const [doctor, setDoctor] = useState(null);
  const [date, setDate] = useState("");
  const [time, setTime] = useState(null);
  const [confirmed, setConfirmed] = useState(false);

  const doctorsInDept = mockDoctors.filter((d) => d.specialization === department);

  const stepLabel = (n, label) => (
    <div className={`step ${step > n ? "done" : step === n ? "active" : ""}`}>{label}</div>
  );

  const handleConfirm = () => {
    // TODO: replace with patientApi.bookAppointment({ doctor_id, date, time, reason })
    setConfirmed(true);
  };

  if (confirmed) {
    return (
      <div className="page">
        <div className="card" style={{ maxWidth: 480, margin: "40px auto", textAlign: "center" }}>
          <span className="badge badge-success" style={{ marginBottom: 12 }}>Appointment booked</span>
          <h2>{doctor.name}</h2>
          <p>{doctor.specialization}</p>
          <p style={{ fontWeight: 600, color: "var(--ink)" }}>{date} · {time}</p>
          <p>The doctor has been notified.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Book an appointment</h1>
      </div>
      <PulseDivider />

      <div className="steps">
        {stepLabel(1, "Department")}
        {stepLabel(2, "Doctor")}
        {stepLabel(3, "Date & time")}
      </div>

      {step === 1 && (
        <div className="grid grid-3">
          {DEPARTMENTS.map((dept) => (
            <div
              key={dept}
              className="card card-hover"
              style={{ cursor: "pointer" }}
              onClick={() => { setDepartment(dept); setStep(2); }}
            >
              <h3>{dept}</h3>
              <p>{mockDoctors.filter((d) => d.specialization === dept).length} doctor(s) available</p>
            </div>
          ))}
        </div>
      )}

      {step === 2 && (
        <div className="grid grid-2">
          {doctorsInDept.map((doc) => (
            <div
              key={doc.id}
              className="card card-hover"
              style={{ cursor: "pointer" }}
              onClick={() => { setDoctor(doc); setStep(3); }}
            >
              <h3>{doc.name}</h3>
              <p style={{ margin: "4px 0" }}>⭐ {doc.rating} · {doc.visiting_hours}</p>
              <p style={{ margin: 0 }}>Available: {doc.available_days.join(", ")}</p>
            </div>
          ))}
          <button className="btn btn-ghost" onClick={() => setStep(1)}>← Back to departments</button>
        </div>
      )}

      {step === 3 && (
        <div className="card" style={{ maxWidth: 480 }}>
          <h3>{doctor.name} — {doctor.specialization}</h3>
          <div className="field">
            <label>Date</label>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} min="2026-07-02" />
          </div>
          <div className="field">
            <label>Time slot</label>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {mockSlots.map((slot) => (
                <button
                  key={slot}
                  type="button"
                  className={time === slot ? "btn btn-primary" : "btn btn-secondary"}
                  onClick={() => setTime(slot)}
                >
                  {slot}
                </button>
              ))}
            </div>
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
            <button className="btn btn-ghost" onClick={() => setStep(2)}>← Back</button>
            <button className="btn btn-primary" disabled={!date || !time} onClick={handleConfirm}>
              Confirm appointment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}