import { Link } from "react-router-dom";
import { Logo, ThemeToggle } from "../components/ui";

const FEATURES = [
  [
    "Read your past papers",
    "Upload PDFs of previous question papers. ExamSync extracts each question with its marks, section and page.",
  ],
  [
    "See the real pattern",
    "Marks distribution, topic frequency, unit coverage and repeated concepts — counted exactly, not guessed.",
  ],
  [
    "Practise on a fresh paper",
    "Generate a new sample paper that follows the structure of your university's past papers and your current syllabus.",
  ],
];
const STEPS = [
  "Create a project for your subject",
  "Upload previous papers",
  "Review the pattern analysis",
  "Add your syllabus and generate a practice paper",
];

export default function Landing() {
  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-4 py-5 sm:px-8">
        <Logo />
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link to="/login" className="btn-ghost">
            Log in
          </Link>
          <Link to="/signup" className="btn-primary hidden sm:inline-flex">
            Get started
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-4 pb-20 pt-16 sm:px-8 sm:pt-24">
        <p className="mb-4 text-sm font-medium text-brand">For university and college exams</p>
        <h1 className="max-w-3xl font-display text-4xl leading-[1.1] tracking-tight sm:text-6xl">
          Stop guessing what the exam looks like.
        </h1>
        <p className="mt-6 max-w-xl text-lg text-muted">
          ExamSync studies your previous question papers, shows you how your exam is actually
          structured, and builds practice papers in the same style.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/signup" className="btn-primary px-5 py-2.5">
            Create free account
          </Link>
          <a href="#how" className="btn-ghost px-5 py-2.5">
            How it works
          </a>
        </div>
      </section>

      <section className="border-y border-line bg-surface">
        <div className="mx-auto grid max-w-6xl gap-px px-4 py-14 sm:px-8 md:grid-cols-3 md:gap-10">
          {FEATURES.map(([t, d]) => (
            <div key={t} className="py-4">
              <h3 className="font-display text-xl">{t}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{d}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="how" className="mx-auto max-w-6xl px-4 py-20 sm:px-8">
        <h2 className="font-display text-3xl tracking-tight">How it works</h2>
        <ol className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map((s, i) => (
            <li key={s} className="card p-5">
              <span className="font-display text-2xl text-brand">{i + 1}</span>
              <p className="mt-2 text-sm">{s}</p>
            </li>
          ))}
        </ol>
      </section>

      <footer className="border-t border-line px-4 py-8 text-center text-xs text-muted sm:px-8">
        ExamSync generates AI sample papers for practice only. Past patterns are not a prediction,
        and generated questions are never official or guaranteed to appear in an exam.
      </footer>
    </div>
  );
}
