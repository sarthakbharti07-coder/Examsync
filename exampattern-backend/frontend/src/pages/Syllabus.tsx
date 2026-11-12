
import { useEffect, useState } from "react";
import { errorMessage } from "../lib/api";
import { projectsApi, type Project } from "../services/projects";
import {
  syllabusApi,
  type Syllabus,
  type SyllabusUnit,
  type SyllabusTopic,
} from "../services/syllabus";

export default function SyllabusPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [projectId, setProjectId] = useState("");
  const [syllabuses, setSyllabuses] = useState<Syllabus[]>([]);
  const [syllabusId, setSyllabusId] = useState("");

  const [units, setUnits] = useState<SyllabusUnit[]>([]);
  const [topics, setTopics] = useState<SyllabusTopic[]>([]);

  const [syllabusTitle, setSyllabusTitle] = useState("");
  const [unitName, setUnitName] = useState("");
  const [topicInputs, setTopicInputs] = useState<Record<string, string>>({});

  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingSyllabuses, setLoadingSyllabuses] = useState(false);
  const [loadingContent, setLoadingContent] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

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
      .catch((err) => setError(errorMessage(err)))
      .finally(() => setLoadingProjects(false));
  }, []);

  // Load syllabuses whenever the project changes
  useEffect(() => {
    if (!projectId) {
      setSyllabuses([]);
      setSyllabusId("");
      return;
    }

    let cancelled = false;

    async function loadSyllabuses() {
      setLoadingSyllabuses(true);
      setError("");
      setSyllabusId("");
      setUnits([]);
      setTopics([]);

      try {
        const data = await syllabusApi.list(projectId);

        if (cancelled) return;

        setSyllabuses(data);
        if (data.length > 0) {
          setSyllabusId(data[0].id);
        }
      } catch (err) {
        if (!cancelled) setError(errorMessage(err));
      } finally {
        if (!cancelled) setLoadingSyllabuses(false);
      }
    }

    loadSyllabuses();

    return () => {
      cancelled = true;
    };
  }, [projectId]);

  // Load units and topics whenever the selected syllabus changes
  useEffect(() => {
    if (!syllabusId) {
      setUnits([]);
      setTopics([]);
      return;
    }

    let cancelled = false;

    async function loadContent() {
      setLoadingContent(true);
      setError("");

      try {
        const loadedUnits = await syllabusApi.listUnits(syllabusId);

        const topicLists = await Promise.all(
          loadedUnits.map((unit) => syllabusApi.listTopics(unit.id)),
        );

        if (cancelled) return;

        setUnits(loadedUnits);
        setTopics(topicLists.flat());
      } catch (err) {
        if (!cancelled) setError(errorMessage(err));
      } finally {
        if (!cancelled) setLoadingContent(false);
      }
    }

    loadContent();

    return () => {
      cancelled = true;
    };
  }, [syllabusId]);

  // Create a syllabus
  async function handleCreateSyllabus(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!projectId || !syllabusTitle.trim()) return;

    setSaving(true);
    setError("");
    setNotice("");

    try {
      const created = await syllabusApi.create(projectId, {
        title: syllabusTitle.trim(),
      });

      setSyllabuses((current) => [created, ...current]);
      setSyllabusTitle("");
      setSyllabusId(created.id);
      setNotice("Syllabus created successfully.");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  // Create a unit
  async function handleAddUnit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!syllabusId || !unitName.trim()) return;

    setSaving(true);
    setError("");
    setNotice("");

    try {
      const created = await syllabusApi.createUnit(syllabusId, {
        name: unitName.trim(),
        position: units.length,
      });

      setUnits((current) => [...current, created]);
      setUnitName("");
      setNotice("Unit added successfully.");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  // Create a topic
  async function handleAddTopic(unitId: string) {
    const name = topicInputs[unitId]?.trim();

    if (!name) return;

    setSaving(true);
    setError("");
    setNotice("");

    try {
      const created = await syllabusApi.createTopic(unitId, {
        name,
        position: topics.filter(
          (topic) => topic.unit_id === unitId,
        ).length,
      });

      setTopics((current) => [...current, created]);
      setTopicInputs((current) => ({ ...current, [unitId]: "" }));
      setNotice("Topic added successfully.");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  // Create a subtopic
  async function handleAddSubtopic(unitId: string, parentId: string) {
    const name = window.prompt("Enter subtopic name:");

    if (!name?.trim()) return;

    setSaving(true);
    setError("");
    setNotice("");

    try {
      const created = await syllabusApi.createTopic(unitId, {
        name: name.trim(),
        parent_topic_id: parentId,
        position: topics.filter(
          (topic) => topic.parent_topic_id === parentId,
        ).length,
      });

      setTopics((current) => [...current, created]);
      setNotice("Subtopic added successfully.");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSaving(false);
    }
  }

  // Rename a unit
  async function handleEditUnit(unit: SyllabusUnit) {
    const name = window.prompt("Enter the new unit name:", unit.name);

    if (!name?.trim() || name.trim() === unit.name) return;

    setError("");

    try {
      const updated = await syllabusApi.updateUnit(unit.id, {
        name: name.trim(),
      });

      setUnits((current) =>
        current.map((item) => item.id === unit.id ? updated : item),
      );
      setNotice("Unit updated successfully.");
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  // Rename a topic
  async function handleEditTopic(topic: SyllabusTopic) {
    const name = window.prompt("Enter the new topic name:", topic.name);

    if (!name?.trim() || name.trim() === topic.name) return;

    setError("");

    try {
      const updated = await syllabusApi.updateTopic(topic.id, {
        name: name.trim(),
      });

      setTopics((current) =>
        current.map((item) => item.id === topic.id ? updated : item),
      );
      setNotice("Topic updated successfully.");
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  // Delete a syllabus
  async function handleDeleteSyllabus() {
    const selected = syllabuses.find((item) => item.id === syllabusId);

    if (!selected || !window.confirm(
      `Delete "${selected.title}" and all its units and topics?`,
    )) return;

    setError("");

    try {
      await syllabusApi.delete(selected.id);

      const remaining = syllabuses.filter((item) => item.id !== selected.id);
      setSyllabuses(remaining);
      setSyllabusId(remaining[0]?.id ?? "");
      setNotice("Syllabus deleted successfully.");
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  // Delete a unit
  async function handleDeleteUnit(unit: SyllabusUnit) {
    if (!window.confirm(
      `Delete "${unit.name}" and all its topics?`,
    )) return;

    setError("");

    try {
      await syllabusApi.deleteUnit(unit.id);

      setUnits((current) => current.filter((item) => item.id !== unit.id));
      setTopics((current) => current.filter((item) => item.unit_id !== unit.id));
      setNotice("Unit deleted successfully.");
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  // Delete a topic and its nested subtopics
  async function handleDeleteTopic(topic: SyllabusTopic) {
    if (!window.confirm(
      `Delete "${topic.name}" and its subtopics?`,
    )) return;

    const idsToDelete = new Set<string>([topic.id]);
    let changed = true;

    while (changed) {
      changed = false;

      topics.forEach((item) => {
        if (
          item.parent_topic_id &&
          idsToDelete.has(item.parent_topic_id) &&
          !idsToDelete.has(item.id)
        ) {
          idsToDelete.add(item.id);
          changed = true;
        }
      });
    }

    setError("");

    try {
      // Delete children before their parents
      const orderedIds = [...idsToDelete].reverse();

      for (const id of orderedIds) {
        await syllabusApi.deleteTopic(id);
      }

      setTopics((current) =>
        current.filter((item) => !idsToDelete.has(item.id)),
      );
      setNotice("Topic deleted successfully.");
    } catch (err) {
      setError(errorMessage(err));
    }
  }

  // Render nested topics
  function renderTopic(
    topic: SyllabusTopic,
    depth = 0,
  ): React.ReactNode {
    const children = topics
      .filter((item) => item.parent_topic_id === topic.id)
      .sort((a, b) => a.position - b.position);

    return (
      <div key={topic.id} className={depth > 0 ? "ml-6 mt-2 border-l border-white/10 pl-3" : "mt-3"}>
        <div className="flex items-center justify-between gap-3 rounded-lg bg-white/[0.03] px-3 py-2">
          <span className="min-w-0 break-words text-sm">
            {topic.name}
          </span>

          <div className="flex shrink-0 gap-3 text-xs">
            <button
              type="button"
              onClick={() => handleAddSubtopic(
                topic.unit_id,
                topic.id,
              )}
              disabled={saving}
              className="text-teal-400 hover:text-teal-300"
            >
              + Subtopic
            </button>

            <button
              type="button"
              onClick={() => handleEditTopic(topic)}
              className="text-slate-400 hover:text-white"
            >
              Edit
            </button>

            <button
              type="button"
              onClick={() => handleDeleteTopic(topic)}
              className="text-red-400 hover:text-red-300"
            >
              Delete
            </button>
          </div>
        </div>

        {children.map((child) => renderTopic(child, depth + 1))}
      </div>
    );
  }

  const selectedSyllabus = syllabuses.find(
    (item) => item.id === syllabusId,
  );

  const totalTopics = topics.length;

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <h1 className="font-display text-2xl font-semibold">
          Syllabus
        </h1>
        <p className="mt-2 text-sm text-muted">
          Organize your examination syllabus into units, topics, and subtopics.
        </p>
      </div>

      {/* Messages */}
      {error && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {notice && (
        <div className="rounded-xl border border-teal-500/20 bg-teal-500/10 p-4 text-sm text-teal-400">
          {notice}
        </div>
      )}

      {/* Project selector */}
      <section className="card space-y-3 p-5">
        <label className="block text-sm font-medium">
          Examination project
        </label>

        {loadingProjects ? (
          <p className="text-sm text-muted">Loading projects...</p>
        ) : projects.length === 0 ? (
          <p className="text-sm text-red-400">
            No projects found. Create an examination project first.
          </p>
        ) : (
          <select
            value={projectId}
            onChange={(event) => setProjectId(event.target.value)}
            className="w-full rounded-xl border border-white/10 bg-slate-900 p-3 text-sm text-white outline-none focus:border-teal-400"
          >
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.title} — {project.course ?? "Course"}
              </option>
            ))}
          </select>
        )}
      </section>

      {/* Create syllabus */}
      <section className="card space-y-4 p-5">
        <div>
          <h2 className="font-display text-lg font-semibold">
            Create syllabus
          </h2>
          <p className="mt-1 text-xs text-muted">
            Start by creating a syllabus for the selected project.
          </p>
        </div>

        <form
          onSubmit={handleCreateSyllabus}
          className="flex flex-col gap-3 sm:flex-row"
        >
          <input
            type="text"
            value={syllabusTitle}
            onChange={(event) => setSyllabusTitle(event.target.value)}
            placeholder="Enter syllabus title, e.g. BCA Semester 3"
            maxLength={255}
            required
            className="min-w-0 flex-1 rounded-xl border border-white/10 bg-slate-900 p-3 text-sm text-white outline-none focus:border-teal-400"
          />

          <button
            type="submit"
            disabled={saving || !projectId || !syllabusTitle.trim()}
            className="rounded-xl bg-teal-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-teal-300 disabled:opacity-50"
          >
            {saving ? "Saving..." : "Create syllabus"}
          </button>
        </form>
      </section>

      {/* Syllabus selection */}
      <section className="card space-y-4 p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="font-display text-lg font-semibold">
              Your syllabuses
            </h2>
            <p className="mt-1 text-xs text-muted">
              Select a syllabus to manage its contents.
            </p>
          </div>

          <span className="rounded-lg bg-white/5 px-3 py-1.5 text-xs text-muted">
            {syllabuses.length} syllabus(es)
          </span>
        </div>

        {loadingSyllabuses ? (
          <p className="text-sm text-muted">Loading syllabuses...</p>
        ) : syllabuses.length === 0 ? (
          <div className="rounded-xl border border-dashed border-white/10 p-8 text-center">
            <p className="text-sm text-muted">
              No syllabus created for this project yet.
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-3 sm:flex-row">
            <select
              value={syllabusId}
              onChange={(event) => setSyllabusId(event.target.value)}
              className="min-w-0 flex-1 rounded-xl border border-white/10 bg-slate-900 p-3 text-sm text-white outline-none focus:border-teal-400"
            >
              {syllabuses.map((syllabus) => (
                <option key={syllabus.id} value={syllabus.id}>
                  {syllabus.title ?? "Untitled syllabus"}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={handleDeleteSyllabus}
              disabled={!syllabusId}
              className="rounded-xl border border-red-500/30 px-4 py-3 text-sm text-red-400 hover:bg-red-500/10 disabled:opacity-50"
            >
              Delete syllabus
            </button>
          </div>
        )}
      </section>

      {/* Syllabus content */}
      {selectedSyllabus && (
        <>
          {/* Summary */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <div className="card p-4">
              <p className="text-xs text-muted">Units</p>
              <p className="mt-2 font-display text-2xl font-semibold">
                {units.length}
              </p>
            </div>

            <div className="card p-4">
              <p className="text-xs text-muted">Topics and subtopics</p>
              <p className="mt-2 font-display text-2xl font-semibold">
                {totalTopics}
              </p>
            </div>

            <div className="card col-span-2 p-4 sm:col-span-1">
              <p className="text-xs text-muted">Source</p>
              <p className="mt-2 text-sm font-semibold capitalize">
                {selectedSyllabus.source}
              </p>
            </div>
          </div>

          {/* Add unit */}
          <section className="card space-y-4 p-5">
            <div>
              <h2 className="font-display text-lg font-semibold">
                Add a unit
              </h2>
              <p className="mt-1 text-xs text-muted">
                Divide your syllabus into chapters or units.
              </p>
            </div>

            <form
              onSubmit={handleAddUnit}
              className="flex flex-col gap-3 sm:flex-row"
            >
              <input
                type="text"
                value={unitName}
                onChange={(event) => setUnitName(event.target.value)}
                placeholder="Enter unit name, e.g. Unit 1 - Introduction"
                maxLength={255}
                required
                className="min-w-0 flex-1 rounded-xl border border-white/10 bg-slate-900 p-3 text-sm text-white outline-none focus:border-teal-400"
              />

              <button
                type="submit"
                disabled={saving || !unitName.trim()}
                className="rounded-xl bg-teal-400 px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-teal-300 disabled:opacity-50"
              >
                Add unit
              </button>
            </form>
          </section>

          {/* Units and topics */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-lg font-semibold">
                Syllabus structure
              </h2>
              <span className="text-xs text-muted">
                {units.length} units
              </span>
            </div>

            {loadingContent ? (
              <div className="card p-8 text-center text-sm text-muted">
                Loading syllabus content...
              </div>
            ) : units.length === 0 ? (
              <div className="card rounded-xl border border-dashed border-white/10 p-8 text-center">
                <p className="text-sm text-muted">
                  No units yet. Add your first unit above.
                </p>
              </div>
            ) : (
              units.map((unit, index) => {
                const rootTopics = topics
                  .filter(
                    (topic) =>
                      topic.unit_id === unit.id &&
                      topic.parent_topic_id === null,
                  )
                  .sort((a, b) => a.position - b.position);

                return (
                  <div key={unit.id} className="card space-y-4 p-5">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <p className="text-xs font-medium text-teal-400">
                          UNIT {index + 1}
                        </p>
                        <h3 className="mt-1 font-display text-base font-semibold">
                          {unit.name}
                        </h3>
                      </div>

                      <div className="flex gap-3 text-xs">
                        <button
                          type="button"
                          onClick={() => handleEditUnit(unit)}
                          className="text-slate-400 hover:text-white"
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() => handleDeleteUnit(unit)}
                          className="text-red-400 hover:text-red-300"
                        >
                          Delete
                        </button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      {rootTopics.length === 0 ? (
                        <p className="text-xs text-muted">
                          No topics added to this unit yet.
                        </p>
                      ) : (
                        rootTopics.map((topic) => renderTopic(topic))
                      )}
                    </div>

                    <form
                      onSubmit={(event) => {
                        event.preventDefault();
                        handleAddTopic(unit.id);
                      }}
                      className="flex flex-col gap-2 border-t border-white/10 pt-4 sm:flex-row"
                    >
                      <input
                        type="text"
                        value={topicInputs[unit.id] ?? ""}
                        onChange={(event) =>
                          setTopicInputs((current) => ({
                            ...current,
                            [unit.id]: event.target.value,
                          }))
                        }
                        placeholder="Enter a topic name"
                        maxLength={500}
                        className="min-w-0 flex-1 rounded-lg border border-white/10 bg-slate-900 p-2.5 text-sm text-white outline-none focus:border-teal-400"
                      />

                      <button
                        type="submit"
                        disabled={saving || !topicInputs[unit.id]?.trim()}
                        className="rounded-lg border border-teal-400/30 px-4 py-2.5 text-sm text-teal-400 hover:bg-teal-400/10 disabled:opacity-50"
                      >
                        + Add topic
                      </button>
                    </form>
                  </div>
                );
              })
            )}
          </section>
        </>
      )}
    </div>
  );
}
