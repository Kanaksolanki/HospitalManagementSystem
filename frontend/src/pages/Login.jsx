import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const result = loginUser(email, password);
    if (!result.success) {
      setError(result.error);
      return;
    }
    navigate(result.user.role === "doctor" ? "/doctor" : "/patient");
  };

  const fillDemo = (role) => {
    if (role === "patient") { setEmail("riya.patient@demo.com"); setPassword("demo123"); }
    else { setEmail("sharma.doctor@demo.com"); setPassword("demo123"); }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div className="card" style={{ width: 380 }}>
        <span className="eyebrow">MediCore</span>
        <h1>Sign in</h1>
        <p style={{ marginBottom: 20 }}>Access your patient or doctor portal.</p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          {error && <p style={{ color: "var(--danger)", fontSize: 13, marginTop: -8 }}>{error}</p>}
          <button type="submit" className="btn btn-primary btn-block">Log in</button>
        </form>

        <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
          <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => fillDemo("patient")}>
            Try as Patient
          </button>
          <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => fillDemo("doctor")}>
            Try as Doctor
          </button>
        </div>

        <p style={{ marginTop: 20, fontSize: 13, textAlign: "center" }}>
          No account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
