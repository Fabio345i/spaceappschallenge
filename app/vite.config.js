import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  define: {
  CESIUM_BASE_URL: JSON.stringify('/cesium')
},
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})
