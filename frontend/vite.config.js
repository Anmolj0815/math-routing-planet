import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // This is the crucial part that fixes the Docker build error
  root: 'frontend',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  }
});
