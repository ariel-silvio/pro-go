import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// GitHub Pages project site: https://ariel-silvio.github.io/pro-go/
export default defineConfig({
  base: '/pro-go/',
  plugins: [react(), tailwindcss()],
});
