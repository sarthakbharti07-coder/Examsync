import { api } from "../lib/api";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
}

// REAL backend endpoints (implemented in backend/app/api/v1/auth.py).
export const authApi = {
  register: (email: string, password: string, full_name?: string) =>
    api
      .post<User>("/auth/register", { email, password, full_name: full_name || null })
      .then((r) => r.data),
  login: (email: string, password: string) =>
    api
      .post<{ access_token: string }>("/auth/login", { email, password })
      .then((r) => r.data.access_token),
  me: () => api.get<User>("/auth/me").then((r) => r.data),
};
