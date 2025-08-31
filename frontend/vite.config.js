import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // GitHub Pages 配置
  base: process.env.NODE_ENV === 'production' ? '/QD-class2/' : '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false
  },
  // 开发服务器配置
  server: {
    host: '0.0.0.0',
    port: 5173,
    open: true
  }
})