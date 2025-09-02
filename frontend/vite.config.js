import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Remove the root: 'public' line - let Vite use default root
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  // Add this to ensure proper path resolution
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  }
});
