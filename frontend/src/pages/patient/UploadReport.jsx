import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { mockPatients } from "../../mock/mockData";
import PulseDivider from "../../components/common/PulseDivider";
import Badge from "../../components/common/Badge";

const REPORT_TYPES = ["Blood Test", "MRI", "X-Ray", "CT Scan", "ECG", "Prescription"];

export default function UploadReport() {
  const { user } = useAuth();
  const patient = mockPatients.find((p) => p.patient_id === user?.displayId);

  const [reportType, setReportType] = useState(REPORT_TYPES[0]);
  const [file, setFile] = useState(null);
  const [reports, setReports] = useState(patient?.reports || []);
  const [processing, setProcessing] = useState(false);

  const handleUpload = (e) => {
    e.preventDefault();
    if (!file || !patient) return;
    setProcessing(true);
    // TODO: replace with patientApi.uploadReport(formData) — backend calls
    // ai-module/report_summarizer.py and returns the ai_summary below.
    setTimeout(() => {
      const newReport = {
        id: Date.now(),
        report_type: reportType,
        date: new Date().toISOString().slice(0, 10),
        hospital: "Uploaded by patient",
        ai_summary: "Report received. Summary will appear once the AI module processes it.",
        flags: [],
      };
      patient.reports.unshift(newReport); // mutate shared record so doctor side sees it too
      setReports([...patient.reports]);
      setFile(null);
      setProcessing(false);
    }, 900);
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Upload report</h1>
        <p>Reports are summarized automatically and stored in your timeline.</p>
      </div>
      <PulseDivider />

      <form onSubmit={handleUpload} className="card" style={{ maxWidth: 480, marginBottom: 32 }}>
        <div className="field">
          <label>Report type</label>
          <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
            {REPORT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="field">
          <label>File (PDF or image)</label>
          <input type="file" accept=".pdf,image/*" onChange={(e) => setFile(e.target.files[0])} />
        </div>
        <button className="btn btn-primary btn-block" disabled={!file || processing}>
          {processing ? "Processing…" : "Upload report"}
        </button>
      </form>

      <h2>Your reports</h2>
      <div className="grid grid-2" style={{ marginTop: 12 }}>
        {reports.map((r) => (
          <div key={r.id} className="card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
              <h3>{r.report_type}</h3>
              {r.flags.length > 0 ? <Badge variant="accent">{r.flags[0]}</Badge> : <Badge variant="success">Clear</Badge>}
            </div>
            <p style={{ margin: "4px 0" }}>{r.date} · {r.hospital}</p>
            <p style={{ fontSize: 13 }}>{r.ai_summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}