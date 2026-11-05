import { execSync } from 'node:child_process';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// Short commit id and build time, shown in the menu so anyone can tell which version they are looking at.
function sha() {
  try { return execSync('git rev-parse --short HEAD').toString().trim(); } catch { return 'local'; }
}
const builtAt = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';

// GitHub Pages project site: https://ariel-silvio.github.io/pro-go/
export default defineConfig({
  base: '/pro-go/',
  plugins: [react(), tailwindcss()],
  define: {
    __BUILD_SHA__: JSON.stringify(process.env.GITHUB_SHA?.slice(0, 7) ?? sha()),
    __BUILD_TIME__: JSON.stringify(builtAt),
  },
});
