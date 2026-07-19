import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { defineConfig } from "vite";
export default defineConfig({
    plugins: [react(), tailwindcss()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
        extensions: [".ts", ".tsx", ".js", ".jsx"],
    },
    define: {
        global: "globalThis", // Fix global polyfill
    },
    optimizeDeps: {
        include: ["maplibre-gl"], // Pre-bundle
        esbuildOptions: {
            target: "es2022",
        },
    },
    esbuild: {
        target: "es2022",
    },
    build: {
        chunkSizeWarningLimit: 1500,
    },
    // Vitest configuration
    test: {
        globals: true,
        environment: "jsdom",
        setupFiles: [],
        include: ["src/**/__tests__/**/*.test.ts", "src/**/__tests__/**/*.test.tsx"],
        coverage: {
            provider: "v8",
            reporter: ["text", "json", "html"],
            include: ["src/services/**"],
        },
    },
});
