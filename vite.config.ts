import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
    server: {
        strictPort: true,
        open: true,
    },
    envPrefix: ["VITE_"],
    plugins: [svelte(), tsconfigPaths()],
});
