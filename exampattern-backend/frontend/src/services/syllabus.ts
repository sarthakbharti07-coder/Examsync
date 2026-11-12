
import { api } from "../lib/api";

// ---------- Types ----------

export interface Syllabus {
  id: string;
  project_id: string;
  document_id: string | null;
  source: "manual" | "upload";
  title: string | null;
  raw_text: string | null;
  coverage_report: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface SyllabusUnit {
  id: string;
  syllabus_id: string;
  name: string;
  position: number;
  created_at: string;
  updated_at: string;
}

export interface SyllabusTopic {
  id: string;
  unit_id: string;
  parent_topic_id: string | null;
  name: string;
  position: number;
  created_at: string;
  updated_at: string;
}

// ---------- Syllabus API ----------

export const syllabusApi = {
  // Get all syllabuses for a project
  list: (projectId: string) =>
    api
      .get<Syllabus[]>(`/syllabus/project/${projectId}`)
      .then((response) => response.data),

  // Create a syllabus
  create: (
    projectId: string,
    data: { title: string; raw_text?: string },
  ) =>
    api
      .post<Syllabus>(`/syllabus/project/${projectId}`, data)
      .then((response) => response.data),

  // Get one syllabus
  get: (syllabusId: string) =>
    api
      .get<Syllabus>(`/syllabus/${syllabusId}`)
      .then((response) => response.data),

  // Update a syllabus
  update: (
    syllabusId: string,
    data: { title?: string; raw_text?: string },
  ) =>
    api
      .patch<Syllabus>(`/syllabus/${syllabusId}`, data)
      .then((response) => response.data),

  // Delete a syllabus
  delete: (syllabusId: string) =>
    api.delete(`/syllabus/${syllabusId}`),

  // ---------- Units ----------

  // Create a unit
  createUnit: (
    syllabusId: string,
    data: { name: string; position?: number },
  ) =>
    api
      .post<SyllabusUnit>(`/syllabus/${syllabusId}/units`, data)
      .then((response) => response.data),

  // Get all units
  listUnits: (syllabusId: string) =>
    api
      .get<SyllabusUnit[]>(`/syllabus/${syllabusId}/units`)
      .then((response) => response.data),

  // Update a unit
  updateUnit: (
    unitId: string,
    data: { name?: string; position?: number },
  ) =>
    api
      .patch<SyllabusUnit>(`/syllabus/units/${unitId}`, data)
      .then((response) => response.data),

  // Delete a unit
  deleteUnit: (unitId: string) =>
    api.delete(`/syllabus/units/${unitId}`),

  // ---------- Topics ----------

  // Create a topic or subtopic
  createTopic: (
    unitId: string,
    data: {
      name: string;
      position?: number;
      parent_topic_id?: string | null;
    },
  ) =>
    api
      .post<SyllabusTopic>(`/syllabus/units/${unitId}/topics`, data)
      .then((response) => response.data),

  // Get all topics for a unit
  listTopics: (unitId: string) =>
    api
      .get<SyllabusTopic[]>(`/syllabus/units/${unitId}/topics`)
      .then((response) => response.data),

  // Update a topic
  updateTopic: (
    topicId: string,
    data: { name?: string; position?: number },
  ) =>
    api
      .patch<SyllabusTopic>(`/syllabus/topics/${topicId}`, data)
      .then((response) => response.data),

  // Delete a topic
  deleteTopic: (topicId: string) =>
    api.delete(`/syllabus/topics/${topicId}`),
};
