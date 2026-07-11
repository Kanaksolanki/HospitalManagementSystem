import { Link } from "react-router-dom";
import { Activity, HeartPulse, Stethoscope, ShieldCheck } from "lucide-react";
import PulseDivider from "../components/common/PulseDivider";

export default function Landing() {
  return (
    <div>
      <nav className="landing-nav">
        <div style={{ display: "flex", alignItems: "center", gap: 10, fontFamily: "var(--font-display)", fontSize: 20 }}>
          <span className="sidebar-brand-icon"><Activity size={18} /></span>
          MediCore
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <Link to="/login" style={{ color: "var(--ink-soft)", fontWeight: 500 }}>Sign in</Link>
          <Link to="/signup" className="btn btn-primary">Create account</Link>
        </div>
      </nav>

      <div className="landing-hero">
        <span className="landing-eyebrow">AI-powered hospital management</span>
        <h1>Clinical care, quietly organized.</h1>
        <p>
          MediCore keeps patient records, prescriptions, and appointments in one calm place —
          with AI summaries on reports and drug-interaction checks doctors can trust.
        </p>
        <PulseDivider active />
        <div style={{ display: "flex", gap: 10 }}>
          <Link to="/signup" className="btn btn-primary">Create an account</Link>
          <Link to="/login" className="btn btn-secondary">Sign in</Link>
        </div>
      </div>

      <div className="landing-features">
        <div className="grid grid-3">
          <div className="card">
            <HeartPulse size={20} color="var(--primary)" style={{ marginBottom: 10 }} />
            <h3>AI report summaries</h3>
            <p>Every uploaded report gets a plain-language summary and flagged abnormalities.</p>
          </div>
          <div className="card">
            <Stethoscope size={20} color="var(--primary)" style={{ marginBottom: 10 }} />
            <h3>Drug interaction checks</h3>
            <p>Prescriptions are checked against known interactions before they can be saved.</p>
          </div>
          <div className="card">
            <ShieldCheck size={20} color="var(--primary)" style={{ marginBottom: 10 }} />
            <h3>Role-based portals</h3>
            <p>Separate, focused surfaces for patients and clinicians — no clutter.</p>
          </div>
        </div>
      </div>
    </div>
  );
}