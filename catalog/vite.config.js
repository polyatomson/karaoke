import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

process.env = {...process.env, ...loadEnv('production', process.cwd())};
// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.VITE_APP_BASE,
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
