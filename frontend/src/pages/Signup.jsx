import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const { registerUser } = useAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState("patient");
  const [form, setForm] = useState({
    name: "", email: "", phone: "", password: "",
    specialization: "", qualification: "", experience: "",
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null); // { pendingApproval, user, detail } once created

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSubmitting(true);

    const payload = { name: form.name, email: form.email, phone: form.phone, password: form.password, role };
    if (role === "doctor") {
      payload.specialization = form.specialization;
      payload.qualification = form.qualification;
      payload.experience = form.experience ? Number(form.experience) : 0;
    }

    const outcome = await registerUser(payload);
    setSubmitting(false);

    if (!outcome.success) {
      // Backend returns field-keyed errors (e.g. {password: [...]}) for
      // validation failures, or a single string for other failures.
      if (typeof outcome.error === "string") setErrors({ _general: outcome.error });
      return;
    }

    if (outcome.pendingApproval) {
      setResult({ pendingApproval: true });
    } else {
      setResult({ pendingApproval: false, user: outcome.user });
    }
  };

  if (result) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
        <div className="card" style={{ width: 380, textAlign: "center" }}>
          <span className="badge badge-success" style={{ marginBottom: 12 }}>Account created</span>
          <h2>Welcome, {form.name.split(" ")[0] || "there"}</h2>
          {result.pendingApproval ? (
            <p style={{ fontSize: 13 }}>
              Your doctor account has been created and is awaiting admin approval.
              You'll be able to log in once a hospital admin approves it.
            </p>
          ) : (
            <>
              <p>Your patient ID has been generated:</p>
              <p className="id-tag" style={{ fontSize: 16, padding: "8px 16px", display: "inline-block", margin: "8px 0 20px" }}>
                {result.user.displayId}
              </p>
            </>
          )}
          <button className="btn btn-primary btn-block" onClick={() => navigate(result.pendingApproval ? "/" : "/patient")}>
            {result.pendingApproval ? "Back to login" : "Go to dashboard"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div className="card" style={{ width: 440 }}>
        <span className="eyebrow">MediCore</span>
        <h1>Create account</h1>
        <p style={{ marginBottom: 20 }}>You'll be given a unique ID once registered.</p>

        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          <button
            type="button"
            className={role === "patient" ? "btn btn-primary" : "btn btn-secondary"}
            style={{ flex: 1 }}
            onClick={() => setRole("patient")}
          >
            I'm a Patient
          </button>
          <button
            type="button"
            className={role === "doctor" ? "btn btn-primary" : "btn btn-secondary"}
            style={{ flex: 1 }}
            onClick={() => setRole("doctor")}
          >
            I'm a Doctor
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="name">Full name</label>
            <input id="name" value={form.name} onChange={update("name")} required />
          </div>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={form.email} onChange={update("email")} required />
            {errors.email && <p style={{ color: "var(--danger)", fontSize: 12 }}>{errors.email[0]}</p>}
          </div>
          <div className="field">
            <label htmlFor="phone">Phone</label>
            <input id="phone" value={form.phone} onChange={update("phone")} required />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={form.password} onChange={update("password")} required />
            {errors.password && (
              <ul style={{ color: "var(--danger)", fontSize: 12, margin: "4px 0 0", paddingLeft: 18 }}>
                {errors.password.map((msg, i) => <li key={i}>{msg}</li>)}
              </ul>
            )}
          </div>

          {role === "doctor" && (
            <>
              <div className="field">
                <label htmlFor="specialization">Specialization</label>
                <input id="specialization" value={form.specialization} onChange={update("specialization")} required
                  placeholder="e.g. Cardiologist" />
                {errors.specialization && <p style={{ color: "var(--danger)", fontSize: 12 }}>{errors.specialization[0]}</p>}
              </div>
              <div className="grid grid-2">
                <div className="field">
                  <label htmlFor="qualification">Qualification</label>
                  <input id="qualification" value={form.qualification} onChange={update("qualification")}
                    placeholder="e.g. MBBS, MD" />
                </div>
                <div className="field">
                  <label htmlFor="experience">Years of experience</label>
                  <input id="experience" type="number" min="0" value={form.experience} onChange={update("experience")} />
                </div>
              </div>
            </>
          )}

          {errors._general && <p style={{ color: "var(--danger)", fontSize: 13 }}>{errors._general}</p>}

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? "Creating account…" : `Create ${role} account`}
          </button>
        </form>

        <p style={{ marginTop: 20, fontSize: 13, textAlign: "center" }}>
          Already have an account? <Link to="/">Log in</Link>
        </p>
      </div>
    </div>
  );
}
