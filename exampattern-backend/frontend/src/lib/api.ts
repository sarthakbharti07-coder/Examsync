import axios, { AxiosError } from "axios";

export const TOKEN_KEY = "examsync_token";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1",
  timeout: 30_000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err: AxiosError) => {
    // An expired/invalid token on a protected call: drop it and let AuthContext react.
    if (err.response?.status === 401 && localStorage.getItem(TOKEN_KEY)) {
      localStorage.removeItem(TOKEN_KEY);
      window.dispatchEvent(new Event("examsync:logout"));
    }
    return Promise.reject(err);
  },
);

/** Turns any thrown error into a user-facing message using the backend's {error:{message}} shape. */
export function errorMessage(e: unknown): string {
  if (axios.isAxiosError(e)) {
    if (!e.response) return "Cannot reach the server. Is the backend running?";
    return e.response.data?.error?.message ?? `Request failed (${e.response.status})`;
  }
  return e instanceof Error ? e.message : "Something went wrong";
}
