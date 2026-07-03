import { createContext, useContext, useState, useEffect } from "react";
import { mockUsers } from "../mock/mockData";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("hms_user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (user) localStorage.setItem("hms_user", JSON.stringify(user));
    else localStorage.removeItem("hms_user");
  }, [user]);

  // TODO: replace with authApi.login() once Diksha's /api/auth/login/ is live.
  // Kept synchronous + mock-based so frontend work isn't blocked on backend.
  const loginUser = (email, password) => {
    const match = mockUsers.find((u) => u.email === email && u.password === password);
    if (!match) return { success: false, error: "Invalid email or password." };
    setUser(match);
    return { success: true, user: match };
  };

  const logoutUser = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
