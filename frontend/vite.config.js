import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Remove the 'root' property or set it to '.'
  // Vite will use the directory where the config is located by default.
  // The 'public' folder will be automatically recognized as the public asset directory.
  // So there is no need to explicitly specify the 'root'
  // and doing so can sometimes cause issues.
  
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
