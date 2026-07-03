import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  return (
    <nav
      style={{
        height: "var(--nav-height)",
        borderBottom: "1px solid var(--border)",
        background: "var(--surface)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}
    >
      <Link
        to={user ? (user.role === "doctor" ? "/doctor" : "/patient") : "/"}
        style={{
          fontFamily: "var(--font-display)",
          fontSize: 20,
          color: "var(--ink)",
          fontWeight: 500,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span style={{ color: "var(--primary)" }}>◆</span> MediCore
      </Link>

      {user && (
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span className="id-tag">{user.displayId}</span>
          <span style={{ fontSize: 14, color: "var(--ink-soft)" }}>{user.name}</span>
          <button className="btn btn-secondary" onClick={handleLogout}>
            Log out
          </button>
        </div>
      )}
    </nav>
  );
}