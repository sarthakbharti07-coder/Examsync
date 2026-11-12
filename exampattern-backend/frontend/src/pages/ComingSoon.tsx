export default function ComingSoon({ title }: { title: string }) {
  return (
    <div className="card p-10 text-center">
      <h1 className="font-display text-2xl">{title}</h1>
      <p className="mt-2 text-sm text-muted">
        This page is not built yet. It will be implemented next.
      </p>
    </div>
  );
}
