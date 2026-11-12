import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { StatCard, MockBadge } from "../components/ui";
import { MOCK_DASHBOARD as MOCK } from "../mocks/dashboard";
import { errorMessage } from "../lib/api";
import { projectsApi, type Project } from "../services/projects";

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[] | null>(null);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    projectsApi
      .list(6)
      .then((p) => {
        setProjects(p.items);
        setTotal(p.total);
      })
      .catch((e) => setError(errorMessage(e)));
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-3xl tracking-tight">Dashboard</h1>
        <p className="mt-1 text-sm text-muted">
          Projects are live from your account. Cards marked “Sample data” are placeholders until
          those backend features ship.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Subjects / projects" value={projects ? total : "—"} />
        <StatCard label="Uploaded papers" value={MOCK.counts.papers} mock />
        <StatCard label="Analyses" value={MOCK.counts.analyses} mock />
        <StatCard label="Practice papers" value={MOCK.counts.generated} mock />
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <section className="card p-5 lg:col-span-3">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-medium">Papers uploaded per month</h2>
            <MockBadge />
          </div>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={MOCK.activity}>
                <CartesianGrid vertical={false} stroke="var(--line)" />
                <XAxis
                  dataKey="month"
                  tickLine={false}
                  axisLine={false}
                  stroke="var(--muted)"
                  fontSize={12}
                />
                <YAxis
                  allowDecimals={false}
                  tickLine={false}
                  axisLine={false}
                  stroke="var(--muted)"
                  fontSize={12}
                  width={28}
                />
                <Tooltip
                  cursor={{ fill: "var(--line)", opacity: 0.4 }}
                  contentStyle={{
                    background: "var(--surface)",
                    border: "1px solid var(--line)",
                    borderRadius: 8,
                    color: "var(--ink)",
                  }}
                />
                <Bar dataKey="uploads" fill="var(--brand)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card p-5 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-medium">Recent activity</h2>
            <MockBadge />
          </div>
          <ul className="divide-y divide-line">
            {MOCK.recent.map((r) => (
              <li key={r.id} className="py-3">
                <p className="text-xs text-muted">
                  {r.kind} · {r.when}
                </p>
                <p className="text-sm">{r.title}</p>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <section className="card p-5">
        <h2 className="mb-4 font-medium">Your projects</h2>
        {error && (
          <p role="alert" className="text-sm text-red-600 dark:text-red-400">
            {error}
          </p>
        )}
        {!error && projects === null && <p className="text-sm text-muted">Loading…</p>}
        {projects?.length === 0 && (
          <p className="text-sm text-muted">
            No projects yet. Project creation arrives with the Upload page.
          </p>
        )}
        <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {projects?.map((p) => (
            <li key={p.id} className="rounded-lg border border-line p-4">
              <p className="font-medium">{p.title}</p>
              <p className="mt-1 text-xs text-muted">
                {[p.subject?.name, p.course, p.semester && `Sem ${p.semester}`]
                  .filter(Boolean)
                  .join(" · ") || "No details"}
              </p>
            </li>
          ))}
        </ul>
        {total > 6 && (
          <Link to="/app/history" className="mt-4 inline-block text-sm text-brand underline">
            View all {total}
          </Link>
        )}
      </section>
    </div>
  );
}
