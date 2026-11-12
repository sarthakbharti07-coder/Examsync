import { api } from "../lib/api";

export interface Project {
  id: string;
  title: string;
  course: string | null;
  semester: string | null;
  max_marks: number | null;
  duration_minutes: number | null;
  subject: { name: string } | null;
  institution: { name: string } | null;
  created_at: string;
}
export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// REAL backend endpoints (backend/app/api/v1/projects.py).
export const projectsApi = {
  list: (limit = 20, offset = 0) =>
    api.get<Page<Project>>("/projects", { params: { limit, offset } }).then((r) => r.data),
};
