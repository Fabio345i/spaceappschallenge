import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  define: {
  CESIUM_BASE_URL: JSON.stringify('/cesium')
},
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
})
