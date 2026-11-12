// ⚠ MOCK DATA — placeholder values for UI development only.
// The backend has no document, analysis or paper endpoints yet. Replace these with real
// services (documents.ts, analysis.ts, papers.ts) once those endpoints exist.
export const MOCK_DASHBOARD = {
  counts: { papers: 12, analyses: 3, generated: 5 },
  activity: [
    { month: "Jun", uploads: 2 },
    { month: "Jul", uploads: 4 },
    { month: "Aug", uploads: 3 },
    { month: "Sep", uploads: 6 },
    { month: "Oct", uploads: 5 },
    { month: "Nov", uploads: 7 },
  ],
  recent: [
    { id: "m1", kind: "Analysis", title: "Data Structures — 5 papers", when: "2 days ago" },
    { id: "m2", kind: "Practice paper", title: "Operating Systems — 70 marks", when: "4 days ago" },
    { id: "m3", kind: "Upload", title: "DBMS_2023_endsem.pdf", when: "1 week ago" },
  ],
};
