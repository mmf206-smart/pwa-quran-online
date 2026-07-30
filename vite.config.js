import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'قرآن آنلاین PWA',
        short_name: 'قرآن',
        description: 'وب‌اپلیکیشن هوشمند قرآن کریم',
        theme_color: '#0f172a',
        background_color: '#0f172a',
        display: 'standalone',
        dir: 'rtl',
        lang: 'fa'
      }
    })
  ]
})