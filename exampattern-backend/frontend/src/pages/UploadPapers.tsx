
import { useEffect, useRef, useState } from "react";
import { errorMessage } from "../lib/api";
import { projectsApi, type Project } from "../services/projects";
import {documentsApi,type UploadedDocument,} from "../services/documents";

interface UploadItem {
  id: string;
  file: File;
  progress: number;
  status: "pending" | "uploading" | "success" | "error";
  message?: string;
}

export default function UploadPapers() {
  const inputRef = useRef<HTMLInputElement>(null);

  const [projects, setProjects] = useState<Project[]>([]);
  const [projectId, setProjectId] = useState("");
  const [items, setItems] = useState<UploadItem[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [dragging, setDragging] = useState(false);

  // Load examination projects
  useEffect(() => {
    projectsApi
      .list()
      .then((data) => {
        setProjects(data.items);

        if (data.items.length > 0) {
          setProjectId(data.items[0].id);
        }
      })
      .catch((error) => {
        console.error("Could not load projects:", error);
      })
      .finally(() => setLoadingProjects(false));
  }, []);

  // Add selected PDF files
  function addFiles(files: FileList | File[]) {
    const selected = Array.from(files);

    const valid = selected.filter(
      (file) =>
        file.name.toLowerCase().endsWith(".pdf") &&
        (file.type === "application/pdf" || file.type === ""),
    );

    const invalidCount = selected.length - valid.length;

    if (invalidCount > 0) {
      alert(`${invalidCount} file(s) skipped. Only PDF files are allowed.`);
    }

    const newItems: UploadItem[] = valid.map((file) => ({
      id: crypto.randomUUID(),
      file,
      progress: 0,
      status: "pending",
    }));

    setItems((current) => [...current, ...newItems]);
  }

  // Update individual file status
  function updateItem(id: string, changes: Partial<UploadItem>) {
    setItems((current) =>
      current.map((item) =>
        item.id === id ? { ...item, ...changes } : item,
      ),
    );
  }

  // Upload one PDF
  async function uploadOne(item: UploadItem) {
    updateItem(item.id, {
      status: "uploading",
      progress: 0,
      message: undefined,
    });

    try {
      const result: UploadedDocument = await documentsApi.upload(
        projectId,
        item.file,
        (progress) => updateItem(item.id, { progress }),
      );

      updateItem(item.id, {
        status: "success",
        progress: 100,
        message: result.message,
      });
    } catch (error) {
      updateItem(item.id, {
        status: "error",
        message: errorMessage(error),
      });
    }
  }

  // Upload all pending files
  async function uploadAll() {
    if (!projectId) {
      alert("Please select an examination project.");
      return;
    }

    const pending = items.filter(
      (item) =>
        item.status === "pending" || item.status === "error",
    );

    for (const item of pending) {
      await uploadOne(item);
    }
  }

  const completedCount = items.filter(
    (item) => item.status === "success",
  ).length;

  const busy = items.some(
    (item) => item.status === "uploading",
  );

  return (
    <div className="space-y-6">

      {/* Page heading */}
      <div>
        <h1 className="font-display text-2xl font-semibold">
          Upload question papers
        </h1>

        <p className="mt-2 text-sm text-muted">
          Upload previous-year examination papers for AI-powered analysis.
        </p>
      </div>

      {/* Project selection */}
      <div className="card space-y-4 p-6">
        <label className="block text-sm font-medium">
          Select examination project
        </label>

        {loadingProjects ? (
          <p className="text-sm text-muted">
            Loading projects...
          </p>
        ) : projects.length === 0 ? (
          <p className="text-sm text-red-400">
            No projects found. Create an examination project first.
          </p>
        ) : (
          <select
            value={projectId}
            onChange={(event) => setProjectId(event.target.value)}
            disabled={busy}
            className="w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm text-white outline-none focus:border-teal-400"
          >
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.title} — {project.course ?? "Course"}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* PDF drag and drop area */}
      <div
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          addFiles(event.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={`card flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-12 text-center transition ${
          dragging
            ? "border-teal-400 bg-teal-400/10"
            : "border-white/15 hover:border-teal-400/60"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          hidden
          onChange={(event) => {
            if (event.target.files) {
              addFiles(event.target.files);
            }

            event.target.value = "";
          }}
        />

        <div className="mb-4 rounded-full bg-teal-400/10 p-5 text-3xl text-teal-400">
          ↑
        </div>

        <h2 className="font-display text-lg font-semibold">
          Drag and drop your PDFs here
        </h2>

        <p className="mt-2 text-sm text-muted">
          Or click to browse files from your computer
        </p>

        <p className="mt-4 text-xs text-muted">
          PDF only · Maximum 20 MB per file · Multiple files supported
        </p>
      </div>

      {/* Selected files */}
      {items.length > 0 && (
        <div className="card space-y-4 p-6">

          <div className="flex items-center justify-between">
            <h2 className="font-display text-lg font-semibold">
              Selected files ({items.length})
            </h2>

            <span className="text-xs text-muted">
              {completedCount} uploaded
            </span>
          </div>

          <div className="space-y-3">
            {items.map((item) => (
              <div
                key={item.id}
                className="rounded-xl border border-white/10 p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">
                      {item.file.name}
                    </p>

                    <p className="mt-1 text-xs text-muted">
                      {(item.file.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                  </div>

                  <span
                    className={`shrink-0 text-xs font-medium ${
                      item.status === "success"
                        ? "text-emerald-400"
                        : item.status === "error"
                          ? "text-red-400"
                          : "text-teal-400"
                    }`}
                  >
                    {item.status === "success"
                      ? "Uploaded"
                      : item.status === "error"
                        ? "Failed"
                        : item.status === "uploading"
                          ? `${item.progress}%`
                          : "Pending"}
                  </span>
                </div>

                {/* Upload progress */}
                {item.status === "uploading" && (
                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/10">
                    <div
                      className="h-full rounded-full bg-teal-400 transition-all"
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                )}

                {item.message && (
                  <p className="mt-2 text-xs text-muted">
                    {item.message}
                  </p>
                )}

                {/* Remove pending or failed files */}
                {(item.status === "pending" ||
                  item.status === "error") && (
                  <button
                    type="button"
                    onClick={() =>
                      setItems((current) =>
                        current.filter(
                          (entry) => entry.id !== item.id,
                        ),
                      )
                    }
                    className="mt-2 text-xs text-red-400 hover:text-red-300"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Upload button */}
          <button
            type="button"
            onClick={uploadAll}
            disabled={
              busy ||
              !projectId ||
              projects.length === 0
            }
            className="w-full rounded-xl bg-teal-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-teal-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {busy
              ? "Uploading..."
              : "Upload selected papers"}
          </button>
        </div>
      )}
    </div>
  );
}
