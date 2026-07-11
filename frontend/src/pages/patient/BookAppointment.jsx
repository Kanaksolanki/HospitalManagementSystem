// import { useState } from "react";
// import { mockDoctors, mockSlots } from "../../mock/mockData";
// import PulseDivider from "../../components/common/PulseDivider";

// const DEPARTMENTS = [...new Set(mockDoctors.map((d) => d.specialization))];

// export default function BookAppointment() {
//   const [step, setStep] = useState(1);
//   const [department, setDepartment] = useState(null);
//   const [doctor, setDoctor] = useState(null);
//   const [date, setDate] = useState("");
//   const [time, setTime] = useState(null);
//   const [confirmed, setConfirmed] = useState(false);

//   const doctorsInDept = mockDoctors.filter((d) => d.specialization === department);

//   const stepLabel = (n, label) => (
//     <div className={`step ${step > n ? "done" : step === n ? "active" : ""}`}>{label}</div>
//   );

//   const handleConfirm = () => {
//     // TODO: replace with patientApi.bookAppointment({ doctor_id, date, time, reason })
//     setConfirmed(true);
//   };

//   if (confirmed) {
//     return (
//       <div className="page">
//         <div className="card" style={{ maxWidth: 480, margin: "40px auto", textAlign: "center" }}>
//           <span className="badge badge-success" style={{ marginBottom: 12 }}>Appointment booked</span>
//           <h2>{doctor.name}</h2>
//           <p>{doctor.specialization}</p>
//           <p style={{ fontWeight: 600, color: "var(--ink)" }}>{date} · {time}</p>
//           <p>The doctor has been notified.</p>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="page">
//       <div className="page-header">
//         <span className="eyebrow">Patient Portal</span>
//         <h1>Book an appointment</h1>
//       </div>
//       <PulseDivider />

//       <div className="steps">
//         {stepLabel(1, "Department")}
//         {stepLabel(2, "Doctor")}
//         {stepLabel(3, "Date & time")}
//       </div>

//       {step === 1 && (
//         <div className="grid grid-3">
//           {DEPARTMENTS.map((dept) => (
//             <div
//               key={dept}
//               className="card card-hover"
//               style={{ cursor: "pointer" }}
//               onClick={() => { setDepartment(dept); setStep(2); }}
//             >
//               <h3>{dept}</h3>
//               <p>{mockDoctors.filter((d) => d.specialization === dept).length} doctor(s) available</p>
//             </div>
//           ))}
//         </div>
//       )}

//       {step === 2 && (
//         <div className="grid grid-2">
//           {doctorsInDept.map((doc) => (
//             <div
//               key={doc.id}
//               className="card card-hover"
//               style={{ cursor: "pointer" }}
//               onClick={() => { setDoctor(doc); setStep(3); }}
//             >
//               <h3>{doc.name}</h3>
//               <p style={{ margin: "4px 0" }}>⭐ {doc.rating} · {doc.visiting_hours}</p>
//               <p style={{ margin: 0 }}>Available: {doc.available_days.join(", ")}</p>
//             </div>
//           ))}
//           <button className="btn btn-ghost" onClick={() => setStep(1)}>← Back to departments</button>
//         </div>
//       )}

//       {step === 3 && (
//         <div className="card" style={{ maxWidth: 480 }}>
//           <h3>{doctor.name} — {doctor.specialization}</h3>
//           <div className="field">
//             <label>Date</label>
//             <input type="date" value={date} onChange={(e) => setDate(e.target.value)} min="2026-07-02" />
//           </div>
//           <div className="field">
//             <label>Time slot</label>
//             <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
//               {mockSlots.map((slot) => (
//                 <button
//                   key={slot}
//                   type="button"
//                   className={time === slot ? "btn btn-primary" : "btn btn-secondary"}
//                   onClick={() => setTime(slot)}
//                 >
//                   {slot}
//                 </button>
//               ))}
//             </div>
//           </div>
//           <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
//             <button className="btn btn-ghost" onClick={() => setStep(2)}>← Back</button>
//             <button className="btn btn-primary" disabled={!date || !time} onClick={handleConfirm}>
//               Confirm appointment
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }


import { useState } from "react";
import { Check } from "lucide-react";
import { mockDoctors, mockSlots } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";

const DEPARTMENTS = [...new Set(mockDoctors.map((d) => d.specialization))];

function Stepper({ step }) {
  const items = [
    { n: 1, label: "Department" },
    { n: 2, label: "Doctor" },
    { n: 3, label: "Date & time" },
  ];
  return (
    <div className="stepper">
      {items.map((item, i) => {
        const state = step > item.n ? "done" : step === item.n ? "active" : "";
        return (
          <div key={item.n} style={{ display: "flex", alignItems: "center", flex: i < items.length - 1 ? 1 : "initial" }}>
            <div className="stepper-item">
              <span className={`stepper-circle ${state}`}>
                {step > item.n ? <Check size={14} /> : item.n}
              </span>
              <span className={`stepper-label ${state}`}>{item.label}</span>
            </div>
            {i < items.length - 1 && <div className="stepper-line" />}
          </div>
        );
      })}
    </div>
  );
}

export default function BookAppointment() {
  const [step, setStep] = useState(1);
  const [department, setDepartment] = useState(null);
  const [doctor, setDoctor] = useState(null);
  const [date, setDate] = useState("");
  const [time, setTime] = useState(null);
  const [reason, setReason] = useState("Consultation");
  const [confirmed, setConfirmed] = useState(false);

  const doctorsInDept = mockDoctors.filter((d) => d.specialization === department);

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
        <p>Three quick steps: pick a department, then a doctor, then a slot.</p>
      </div>
      <PulseDivider />

      <Stepper step={step} />

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
          <button className="btn btn-ghost" onClick={() => setStep(1)}>← Change department</button>
        </div>
      )}

      {step === 3 && (
        <div className="card" style={{ maxWidth: 700 }}>
          <h3>Pick date &amp; time</h3>
          <p style={{ marginBottom: 16 }}>With {doctor.name}</p>

          <div className="grid grid-2" style={{ marginBottom: 16 }}>
            <div className="field" style={{ margin: 0 }}>
              <label>Date</label>
              <input type="date" value={date} onChange={(e) => setDate(e.target.value)} min="2026-07-02" />
            </div>
            <div className="field" style={{ margin: 0 }}>
              <label>Reason for visit</label>
              <input value={reason} onChange={(e) => setReason(e.target.value)} />
            </div>
          </div>

          <label style={{ fontSize: 13, fontWeight: 600, color: "var(--ink-soft)", display: "block", marginBottom: 8 }}>
            Available slots
          </label>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 20 }}>
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

          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <button className="btn btn-ghost" onClick={() => setStep(2)}>← Change doctor</button>
            <button className="btn btn-primary" disabled={!date || !time} onClick={handleConfirm}>
              Confirm appointment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}