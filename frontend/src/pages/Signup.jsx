import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function nextId(role) {
  const prefix = role === "doctor" ? "DOC" : "PID";
  const random = Math.floor(1000 + Math.random() * 8999);
  return `${prefix}${String(random).padStart(6, "0")}`;
}

export default function Signup() {
  const [role, setRole] = useState("patient");
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "" });
  const [created, setCreated] = useState(null);
  const navigate = useNavigate();

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: replace with authApi.register({ ...form, role }) once backend is live.
    setCreated(nextId(role));
  };

  if (created) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
        <div className="card" style={{ width: 380, textAlign: "center" }}>
          <span className="badge badge-success" style={{ marginBottom: 12 }}>Account created</span>
          <h2>Welcome, {form.name.split(" ")[0] || "there"}</h2>
          <p>Your {role} ID has been generated:</p>
          <p className="id-tag" style={{ fontSize: 16, padding: "8px 16px", display: "inline-block", margin: "8px 0 20px" }}>
            {created}
          </p>
          {role === "doctor" && (
            <p style={{ fontSize: 13 }}>Doctor accounts require admin approval before login is active.</p>
          )}
          <Link to="/" className="btn btn-primary btn-block">Go to login</Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div className="card" style={{ width: 420 }}>
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
          </div>
          <div className="field">
            <label htmlFor="phone">Phone</label>
            <input id="phone" value={form.phone} onChange={update("phone")} required />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={form.password} onChange={update("password")} required />
          </div>
          <button type="submit" className="btn btn-primary btn-block">
            Create {role} account
          </button>
        </form>

        <p style={{ marginTop: 20, fontSize: 13, textAlign: "center" }}>
          Already have an account? <Link to="/">Log in</Link>
        </p>
      </div>
    </div>
  );
}