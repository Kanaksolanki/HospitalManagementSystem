import { useState, useEffect } from "react";
import { Paperclip } from "lucide-react";
import { uploadReport, getMyReports } from "../../api/patientApi";
import PulseDivider from "../../components/common/PulseDivider";
import Badge from "../../components/common/Badge";

const REPORT_TYPES = ["Blood Test", "MRI", "X-Ray", "CT Scan", "ECG", "Prescription"];

export default function UploadReport() {
  const [reportType, setReportType] = useState(REPORT_TYPES[0]);
  const [file, setFile] = useState(null);
  // Optional now that OCR runs automatically on the uploaded file (see
  // ai-module/ocr_extractor.py). Only needed as a manual override if OCR
  // misreads something or the file is unreadable.
  const [rawText, setRawText] = useState("");
  const [reports, setReports] = useState([]);
  const [loadingReports, setLoadingReports] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [ocrWarning, setOcrWarning] = useState("");

  useEffect(() => {
    getMyReports()
      .then((res) => setReports(res.data))
      .catch(() => setError("Couldn't load your existing reports. Is the backend running?"))
      .finally(() => setLoadingReports(false));
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setProcessing(true);
    setError("");
    setOcrWarning("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("report_type", reportType);
      formData.append("hospital", "Uploaded by patient");
      if (rawText.trim()) formData.append("raw_text", rawText);

      const { data } = await uploadReport(formData);
      setReports((prev) => [data, ...prev]);
      setFile(null);
      setRawText("");
      if (data.ocr_error) {
        setOcrWarning(`Couldn't read the file automatically: ${data.ocr_error}. Try typing the values in manually.`);
      } else if (!data.raw_text) {
        setOcrWarning("No readable text was found in that file. Try a clearer photo, or type the values in manually.");
      }
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        "Upload failed. Make sure the backend is running and you're logged in as a patient."
      );
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Patient Portal</span>
        <h1>Upload a medical report</h1>
        <p>We'll read the file automatically (OCR) and flag anything unusual.</p>
      </div>
      <PulseDivider />

      <form onSubmit={handleUpload} className="card" style={{ marginBottom: 32 }}>
        <div className="grid grid-2" style={{ alignItems: "end" }}>
          <div className="field" style={{ margin: 0 }}>
            <label>Report type</label>
            <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
              {REPORT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="field" style={{ margin: 0 }}>
            <label>Upload file</label>
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <label className="btn btn-secondary" style={{ cursor: "pointer" }}>
                <Paperclip size={15} /> Choose file
                <input type="file" accept=".pdf,image/*" style={{ display: "none" }} onChange={(e) => setFile(e.target.files[0])} />
              </label>
              <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{file ? file.name : "No file selected"}</span>
            </div>
          </div>
        </div>

        <div className="field">
          <label>Manual override (optional — only needed if OCR misreads your file)</label>
          <textarea
            rows={3}
            placeholder={"Leave blank to let OCR read the file automatically.\ne.g. Hemoglobin: 10.1 g/dL"}
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
          />
        </div>

        {ocrWarning && <p style={{ color: "var(--warning, #a15c00)", fontSize: 13 }}>{ocrWarning}</p>}
        {error && <p style={{ color: "var(--danger)", fontSize: 13 }}>{error}</p>}

        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 16 }}>
          <button className="btn btn-primary" disabled={!file || processing}>
            {processing ? "Processing…" : "Upload & summarize"}
          </button>
        </div>
      </form>

      <h2>Your reports</h2>
      {loadingReports ? (
        <p>Loading…</p>
      ) : reports.length === 0 ? (
        <p>No reports uploaded yet.</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 12 }}>
          {reports.map((r) => (
            <div key={r.id} className="card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", flexWrap: "wrap", gap: 8 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <h3 style={{ margin: 0 }}>{r.report_type}</h3>
                  <Badge variant="neutral">{r.uploaded_date}</Badge>
                  {r.ocr_method === "image_ocr" && <Badge variant="neutral">Read via photo OCR</Badge>}
                  {r.ocr_method === "pdf_ocr" && <Badge variant="neutral">Read via scanned-PDF OCR</Badge>}
                </div>
                <span style={{ fontSize: 13, color: "var(--ink-faint)" }}>{r.file?.split("/").pop()}</span>
              </div>
              <p style={{ margin: "8px 0 0" }}>{r.ai_summary || "No summary available for this report."}</p>
              {r.ai_flags?.length > 0 && (
                <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {r.ai_flags.map((f, i) => <Badge key={i} variant="danger">{f}</Badge>)}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
