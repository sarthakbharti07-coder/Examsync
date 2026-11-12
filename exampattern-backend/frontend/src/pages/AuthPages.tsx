import { useState, type FormEvent } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { errorMessage } from "../lib/api";
import { Logo, ThemeToggle } from "../components/ui";

export default function AuthPage({ mode }: { mode: "login" | "signup" }) {
  const { user, login, signup } = useAuth();
  const navigate = useNavigate();
  const from = (useLocation().state as { from?: string } | null)?.from ?? "/app";
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const isLogin = mode === "login";

  if (user) return <Navigate to="/app" replace />;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (isLogin) await login(form.email, form.password);
      else await signup(form.email, form.password, form.name);
      navigate(from, { replace: true });
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="grid min-h-screen place-items-center px-4">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <div className="w-full max-w-sm">
        <Link to="/" className="mb-8 flex justify-center">
          <Logo />
        </Link>
        <form onSubmit={submit} className="card space-y-4 p-6">
          <h1 className="font-display text-2xl">
            {isLogin ? "Welcome back" : "Create your account"}
          </h1>
          {!isLogin && (
            <input
              className="input"
              placeholder="Full name (optional)"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          )}
          <input
            className="input"
            type="email"
            required
            placeholder="Email"
            autoComplete="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <input
            className="input"
            type="password"
            required
            minLength={isLogin ? 1 : 8}
            placeholder={isLogin ? "Password" : "Password (8+ characters)"}
            autoComplete={isLogin ? "current-password" : "new-password"}
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          {error && (
            <p role="alert" className="text-sm text-red-600 dark:text-red-400">
              {error}
            </p>
          )}
          <button className="btn-primary w-full" disabled={busy}>
            {busy ? "Please wait…" : isLogin ? "Log in" : "Sign up"}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-muted">
          {isLogin ? "New here? " : "Already have an account? "}
          <Link className="text-brand underline" to={isLogin ? "/signup" : "/login"}>
            {isLogin ? "Create an account" : "Log in"}
          </Link>
        </p>
      </div>
    </div>
  );
}
