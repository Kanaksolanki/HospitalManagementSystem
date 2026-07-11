// import { useAuth } from "../../context/AuthContext";
// import { mockPatients } from "../../mock/mockData";
// import PulseDivider from "../../components/common/PulseDivider";
// import EmptyState from "../../components/common/EmptyState";

// export default function PrescriptionHistory() {
//   const { user } = useAuth();
//   const patient = mockPatients.find((p) => p.patient_id === user?.displayId);
//   const prescriptions = patient?.prescriptions || [];

//   return (
//     <div className="page">
//       <div className="page-header">
//         <span className="eyebrow">Patient Portal</span>
//         <h1>Prescription history</h1>
//       </div>
//       <PulseDivider />

//       {prescriptions.length === 0 ? (
//         <EmptyState title="No prescriptions yet" message="Prescriptions from your visits will appear here." />
//       ) : (
//         <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
//           {prescriptions.map((p) => (
//             <div key={p.id} className="card">
//               <div style={{ display: "flex", justifyContent: "space-between" }}>
//                 <h3>{p.doctor_name}</h3>
//                 <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{p.date}</span>
//               </div>
//               <div style={{ display: "flex", flexWrap: "wrap", gap: 8, margin: "10px 0" }}>
//                 {p.medicines.map((m, i) => (
//                   <span key={i} className="badge badge-primary">
//                     {m.name} · {m.dosage} · {m.frequency}
//                   </span>
//                 ))}
//               </div>
//               <p style={{ fontSize: 13 }}>{p.notes}</p>
//               {p.followup_date && (
//                 <p style={{ fontSize: 13, fontWeight: 600, color: "var(--ink)" }}>
//                   Follow-up: {p.followup_date}
//                 </p>
//               )}
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }


import { useAuth } from "../../context/AuthContext";
import { mockPatients } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";
import EmptyState from "../../components/common/EmptyState";
import Badge from "../../components/common/Badge";

export default function PrescriptionHistory() {
  const { user } = useAuth();
  const patient = mockPatients.find((p) => p.patient_id === user?.displayId);
  const prescriptions = patient?.prescriptions || [];

  // group by doctor
  const grouped = prescriptions.reduce((acc, p) => {
    acc[p.doctor_name] = acc[p.doctor_name] || { ...p, items: [] };
    acc[p.doctor_name].items.push(p);
    return acc;
  }, {});

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Prescription history</h1>
        <p>Past prescriptions, grouped by the doctor who wrote them.</p>
      </div>
      <PulseDivider />

      {prescriptions.length === 0 ? (
        <EmptyState title="No prescriptions yet" message="Prescriptions from your visits will appear here." />
      ) : (
        Object.values(grouped).map((group) => (
          <div key={group.doctor_name} style={{ marginBottom: 28 }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 10 }}>
              <h3 style={{ margin: 0 }}>{group.doctor_name}</h3>
              <span className="id-tag">{group.doctor_id}</span>
              <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>· {group.specialization}</span>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {group.items.map((p) => (
                <div key={p.id} className="card">
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 }}>
                    <span className="id-tag">{p.id}</span>
                    <Badge variant="neutral">Written {p.date}</Badge>
                    {p.followup_date && <Badge variant="accent">Follow-up {p.followup_date}</Badge>}
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 10 }}>
                    {p.medicines.map((m, i) => (
                      <span key={i} className="badge badge-primary">
                        {m.name} · {m.dosage} · {m.frequency}
                      </span>
                    ))}
                  </div>
                  <p style={{ margin: 0 }}>{p.notes}</p>
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}