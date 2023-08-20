import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import tsconfigPaths from "vite-tsconfig-paths";
import mkcert from "vite-plugin-mkcert";

export default defineConfig({
    server: {
        strictPort: true,
        open: true,
        https: true,
    },
    envPrefix: ["VITE_"],
    plugins: [svelte(), tsconfigPaths(), mkcert()],
});
