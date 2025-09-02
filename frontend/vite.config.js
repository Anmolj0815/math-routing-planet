import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Remove the 'root' property. Vite will default to the directory
  // where the config file is located, which is `frontend`.
  //
  // Alternatively, you can explicitly set it:
  // root: '.',

  build: {
    // The build output should go to the `dist` folder inside the
    // `frontend` directory.
    outDir: 'dist',
    emptyOutDir: true,
  },
});
