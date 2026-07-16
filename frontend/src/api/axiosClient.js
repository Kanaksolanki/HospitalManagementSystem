import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
});

// These endpoints are meant to be called while logged out, so never attach
// a token to them. This matters because DRF's JWT authentication rejects a
// request with a *bad* token (expired/invalid) with a hard 401 before the
// view's permission_classes are even checked -- so a stale token sitting in
// localStorage from a previous session would otherwise break login/signup
// themselves, which should always work regardless of auth state.
const PUBLIC_ENDPOINTS = ["/auth/login/", "/auth/register/", "/auth/token/refresh/"];

axiosClient.interceptors.request.use((config) => {
  const isPublic = PUBLIC_ENDPOINTS.some((path) => config.url?.startsWith(path));
  if (!isPublic) {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// If a request fails because the access token is expired/invalid, clear the
// stale session locally instead of leaving the user stuck in a state where
// every authenticated call 401s. (This doesn't attempt a silent refresh --
// simple and predictable is better here than a refresh loop that can itself
// fail silently.)
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401 && !PUBLIC_ENDPOINTS.some((p) => error.config?.url?.startsWith(p))) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("hms_user");
    }
    return Promise.reject(error);
  }
);

export default axiosClient;