import { createContext, useContext, useState, useEffect } from "react";
import { login as loginRequest, register as registerRequest, logout as logoutRequest, getMe } from "../api/authApi";

const AuthContext = createContext(null);

function ageFromDob(dobStr) {
  if (!dobStr) return null;
  const dob = new Date(dobStr);
  const diffMs = Date.now() - dob.getTime();
  return Math.floor(diffMs / (1000 * 60 * 60 * 24 * 365.25));
}

// Reshapes the backend's /api/auth/me/ response (id, username, role, profile: {...})
// into the flatter `user` shape the existing pages already read (name,
// displayId, blood_group, specialization, etc) -- so pages don't need to
// change just because auth got wired to the real API.
function buildUser(me) {
  const profile = me.profile || {};
  const name = [me.first_name, me.last_name].filter(Boolean).join(" ") || me.username;

  const base = { id: me.id, name, email: me.email, role: me.role, phone: me.phone };

  if (me.role === "patient") {
    return {
      ...base,
      displayId: profile.patient_id,
      age: ageFromDob(profile.dob),
      gender: profile.gender === "F" ? "Female" : profile.gender === "M" ? "Male" : profile.gender,
      blood_group: profile.blood_group,
      allergies: profile.allergies,
    };
  }
  if (me.role === "doctor") {
    return {
      ...base,
      displayId: profile.doctor_id,
      specialization: profile.specialization,
      rating: profile.rating,
    };
  }
  return base;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("hms_user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (user) localStorage.setItem("hms_user", JSON.stringify(user));
    else localStorage.removeItem("hms_user");
  }, [user]);

  const registerUser = async (formData) => {
    try {
      const { data } = await registerRequest(formData);

      // Doctor accounts don't get usable tokens until a hospital admin
      // approves them (see accounts/views.py RegisterView) -- surface that
      // instead of trying to log them in.
      if (formData.role === "doctor") {
        return { success: true, pendingApproval: true, detail: data.detail };
      }

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      const { data: me } = await getMe();
      const builtUser = buildUser(me);
      setUser(builtUser);
      return { success: true, pendingApproval: false, user: builtUser };
    } catch (err) {
      const fieldErrors = err?.response?.data;
      const firstError =
        typeof fieldErrors === "object" && fieldErrors
          ? Object.values(fieldErrors).flat()[0]
          : null;
      return {
        success: false,
        error:
          firstError ||
          (err?.code === "ERR_NETWORK"
            ? "Can't reach the backend. Is it running on http://localhost:8000?"
            : "Something went wrong creating your account."),
      };
    }
  };

  const loginUser = async (email, password) => {
    try {
      const { data: tokens } = await loginRequest({ email, password });
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);

      const { data: me } = await getMe();
      const builtUser = buildUser(me);
      setUser(builtUser);
      return { success: true, user: builtUser };
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        (err?.code === "ERR_NETWORK"
          ? "Can't reach the backend. Is it running on http://localhost:8000?"
          : "Invalid email or password.");
      return { success: false, error: detail };
    }
  };

  const logoutUser = () => {
    const refreshToken = localStorage.getItem("refresh_token");
    setUser(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    // Best-effort -- actually revokes the token server-side so it can't be
    // replayed, but the user is logged out locally either way.
    if (refreshToken) logoutRequest(refreshToken).catch(() => {});
  };

  return (
    <AuthContext.Provider value={{ user, loginUser, registerUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
