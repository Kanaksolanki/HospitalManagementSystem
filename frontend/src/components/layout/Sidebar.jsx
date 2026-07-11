// import { Link, useNavigate } from "react-router-dom";
// import { useAuth } from "../../context/AuthContext";

// export default function Navbar() {
//   const { user, logoutUser } = useAuth();
//   const navigate = useNavigate();

//   const handleLogout = () => {
//     logoutUser();
//     navigate("/");
//   };

//   return (
//     <nav
//       style={{
//         height: "var(--nav-height)",
//         borderBottom: "1px solid var(--border)",
//         background: "var(--surface)",
//         display: "flex",
//         alignItems: "center",
//         justifyContent: "space-between",
//         padding: "0 24px",
//         position: "sticky",
//         top: 0,
//         zIndex: 10,
//       }}
//     >
//       <Link
//         to={user ? (user.role === "doctor" ? "/doctor" : "/patient") : "/"}
//         style={{
//           fontFamily: "var(--font-display)",
//           fontSize: 20,
//           color: "var(--ink)",
//           fontWeight: 500,
//           display: "flex",
//           alignItems: "center",
//           gap: 8,
//         }}
//       >
//         <span style={{ color: "var(--primary)" }}>◆</span> MediCore
//       </Link>

//       {user && (
//         <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
//           <span className="id-tag">{user.displayId}</span>
//           <span style={{ fontSize: 14, color: "var(--ink-soft)" }}>{user.name}</span>
//           <button className="btn btn-secondary" onClick={handleLogout}>
//             Log out
//           </button>
//         </div>
//       )}
//     </nav>
//   );
// }

import { NavLink, useNavigate } from "react-router-dom";
import {
  Activity, LayoutDashboard, CalendarPlus, FileUp, Pill,
  Search, MessageCircle, LogOut,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";

const PATIENT_LINKS = [
  { to: "/patient", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/patient/book", label: "Book appointment", icon: CalendarPlus },
  { to: "/patient/upload-report", label: "Upload report", icon: FileUp },
  { to: "/patient/prescriptions", label: "Prescriptions", icon: Pill },
  { to: "/patient/assistant", label: "Assistant", icon: MessageCircle },
];

const DOCTOR_LINKS = [
  { to: "/doctor", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/doctor/search", label: "Search patient", icon: Search },
  { to: "/doctor/assistant", label: "Assistant", icon: MessageCircle },
];

export default function Sidebar() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();
  const links = user?.role === "doctor" ? DOCTOR_LINKS : PATIENT_LINKS;

  const handleLogout = () => {
    logoutUser();
    navigate("/");
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="sidebar-brand-icon"><Activity size={18} /></span>
        MediCore
      </div>

      <div className="sidebar-role-block">
        <span className="sidebar-eyebrow">{user?.role}</span>
        <div className="sidebar-name">{user?.name}</div>
        <div className="sidebar-id">{user?.displayId}</div>
      </div>

      <nav className="sidebar-nav">
        {links.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="sidebar-link" style={{ width: "100%", border: "none", background: "none", cursor: "pointer" }} onClick={handleLogout}>
          <LogOut size={17} />
          Log out
        </button>
      </div>
    </aside>
  );
}