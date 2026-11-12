
import { Navigate, Route, Routes } from "react-router-dom";

import AppShell from "./components/AppShell";
import ProtectedRoute from "./components/ProtectedRoute";

import AuthPage from "./pages/AuthPages";
import ComingSoon from "./pages/ComingSoon";
import Dashboard from "./pages/Dashboard";
import Landing from "./pages/Landing";
import UploadPapers from "./pages/UploadPapers";
import Syllabus from "./pages/Syllabus";

export default function App() {
  return (
    <Routes>
      {/* Public pages */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<AuthPage mode="login" />} />
      <Route path="/signup" element={<AuthPage mode="signup" />} />

      {/* Protected application pages */}
      <Route element={<ProtectedRoute />}>
        <Route path="/app" element={<AppShell />}>
          <Route index element={<Dashboard />} />

          <Route path="upload" element={<UploadPapers />} />
          <Route path="syllabus" element={<Syllabus />} />

          <Route
            path="analysis"
            element={<ComingSoon title="Pattern analysis" />}
          />

          <Route
            path="generate"
            element={<ComingSoon title="Generate paper" />}
          />

          <Route
            path="history"
            element={<ComingSoon title="History" />}
          />

          <Route
            path="settings"
            element={<ComingSoon title="Settings" />}
          />
        </Route>
      </Route>

      {/* Fallback route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
