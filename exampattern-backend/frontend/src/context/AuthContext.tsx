import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { TOKEN_KEY } from "../lib/api";
import { authApi, type User } from "../services/auth";

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
}
const Ctx = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(!!localStorage.getItem(TOKEN_KEY));

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }, []);

  useEffect(() => {
    if (!localStorage.getItem(TOKEN_KEY)) return;
    authApi
      .me()
      .then(setUser)
      .catch(() => localStorage.removeItem(TOKEN_KEY))
      .finally(() => setLoading(false));
  }, []);
  useEffect(() => {
    window.addEventListener("examsync:logout", logout);
    return () => window.removeEventListener("examsync:logout", logout);
  }, [logout]);

  const login = async (email: string, password: string) => {
    localStorage.setItem(TOKEN_KEY, await authApi.login(email, password));
    try {
      setUser(await authApi.me());
    } catch (e) {
      logout();
      throw e;
    }
  };
  const signup = async (email: string, password: string, name?: string) => {
    await authApi.register(email, password, name);
    await login(email, password);
  };

  return <Ctx.Provider value={{ user, loading, login, signup, logout }}>{children}</Ctx.Provider>;
}

export function useAuth() {
  const v = useContext(Ctx);
  if (!v) throw new Error("useAuth must be used inside AuthProvider");
  return v;
}
