import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Logo, ThemeToggle } from "./ui";
import { Menu } from "./icons";

const NAV = [
  { to: "/app", label: "Dashboard", end: true },
  { to: "/app/upload", label: "Upload papers" },
  { to: "/app/syllabus", label: "Syllabus" },
  { to: "/app/analysis", label: "Pattern analysis" },
  { to: "/app/generate", label: "Generate paper" },
  { to: "/app/history", label: "History" },
  { to: "/app/settings", label: "Settings" },
];

export default function AppShell() {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen lg:flex">
      <aside
        className={`${open ? "block" : "hidden"} border-b border-line bg-surface p-4 lg:sticky lg:top-0 lg:block lg:h-screen lg:w-60 lg:shrink-0 lg:border-b-0 lg:border-r`}
      >
        <div className="hidden pb-6 lg:block">
          <Logo />
        </div>
        <nav className="flex flex-col gap-1">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm transition-colors ${isActive ? "bg-brand/10 font-medium text-brand" : "text-muted hover:bg-ink/5 hover:text-ink"}`
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="min-w-0 flex-1">
        <header className="flex items-center justify-between gap-3 border-b border-line px-4 py-3 sm:px-8">
          <div className="flex items-center gap-3">
            <button
              className="btn-ghost px-2.5! lg:hidden"
              aria-label="Menu"
              onClick={() => setOpen(!open)}
            >
              <Menu />
            </button>
            <span className="lg:hidden">
              <Logo />
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-muted sm:inline">
              {user?.full_name || user?.email}
            </span>
            <ThemeToggle />
            <button
              className="btn-ghost"
              onClick={() => {
                logout();
                navigate("/");
              }}
            >
              Log out
            </button>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8 sm:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
