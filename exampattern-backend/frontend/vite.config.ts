import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// Port 3000 matches the backend's default CORS_ORIGINS.
export default defineConfig({ plugins: [react(), tailwindcss()], server: { port: 3000 } });
