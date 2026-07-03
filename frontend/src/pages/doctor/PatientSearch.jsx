import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { mockPatients } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";

export default function PatientSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    // TODO: replace with doctorApi.searchPatient(query)
    const found = mockPatients.filter(
      (p) => p.patient_id.toLowerCase().includes(query.toLowerCase()) ||
             p.name.toLowerCase().includes(query.toLowerCase())
    );
    setResults(found);
    setSearched(true);
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Doctor Portal</span>
        <h1>Search patient</h1>
        <p>Search by patient ID or name to view full history.</p>
      </div>
      <PulseDivider />

      <form onSubmit={handleSearch} style={{ display: "flex", gap: 8, maxWidth: 480, marginBottom: 24 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. PID000145 or patient name"
          style={{ flex: 1, border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "10px 12px" }}
        />
        <button className="btn btn-primary">Search</button>
      </form>

      {searched && results.length === 0 && <p>No patient found for "{query}".</p>}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {results.map((p) => (
          <div
            key={p.patient_id}
            className="card card-hover"
            style={{ cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center" }}
            onClick={() => navigate(`/doctor/history/${p.patient_id}`)}
          >
            <div>
              <h3 style={{ marginBottom: 2 }}>{p.name}</h3>
              <span className="id-tag">{p.patient_id}</span>
              <span style={{ fontSize: 13, color: "var(--ink-soft)", marginLeft: 10 }}>
                {p.age} yrs · {p.gender} · {p.blood_group}
              </span>
            </div>
            <span className="btn btn-secondary">View history →</span>
          </div>
        ))}
      </div>
    </div>
  );
}
