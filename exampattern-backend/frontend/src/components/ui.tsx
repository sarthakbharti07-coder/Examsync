import type { ReactNode } from "react";
import { Moon, Sun } from "./icons";
import { useTheme } from "../lib/theme";

export function ThemeToggle() {
  const { dark, toggle } = useTheme();
  return (
    <button onClick={toggle} aria-label="Toggle dark mode" className="btn-ghost px-2.5!">
      {dark ? <Sun /> : <Moon />}
    </button>
  );
}

/** Marks any UI fed by placeholder data so it can never be mistaken for real results. */
export function MockBadge({ children = "Sample data" }: { children?: ReactNode }) {
  return (
    <span
      title="Placeholder values — the backend endpoint for this does not exist yet"
      className="rounded-full border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 text-[11px] font-medium text-amber-700 dark:text-amber-300"
    >
      {children}
    </span>
  );
}

export function StatCard({
  label,
  value,
  mock,
  hint,
}: {
  label: string;
  value: ReactNode;
  mock?: boolean;
  hint?: string;
}) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm text-muted">{label}</p>
        {mock && <MockBadge />}
      </div>
      <p className="mt-2 font-display text-3xl tracking-tight">{value}</p>
      {hint && <p className="mt-1 text-xs text-muted">{hint}</p>}
    </div>
  );
}

export function Logo() {
  return (
    <span className="flex items-center gap-2 font-display text-lg font-semibold tracking-tight">
      <span className="grid h-7 w-7 place-items-center rounded-md bg-brand text-sm text-brand-ink">
        E
      </span>
      ExamSync
    </span>
  );
}
