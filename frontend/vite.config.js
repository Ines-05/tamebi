import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // Correcting catch-all for aliases (which are top-level paths in the app)
      // This is tricky because React Router handles some paths, but aliases are dynamic.
      // For now, let's just keep /api proxy.
    }
  }
})
