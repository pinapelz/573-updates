import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react-swc'
import { VitePWA } from 'vite-plugin-pwa'
import icons from './public/icons.json'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(),
    VitePWA({
        registerType: 'autoUpdate',
        manifest: {
          name: '573-UPDATES',
          short_name: '573-UPDATES',
          description: 'A scraper and aggregator of information/news for various arcade games. Currently supports various KONAMI/BEMANI and Performai',
          theme_color: '#FD0B78',
          background_color: '#101828',
          display: 'standalone',
          start_url: '/',
          icons: icons.icons
        },
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
          runtimeCaching: [
            {
              urlPattern: ({ request }) => request.destination === 'document',
              handler: 'NetworkFirst',
              options: {
                cacheName: 'html-cache',
              },
            },
            {
              urlPattern: ({ request }) =>
                ['style', 'script', 'worker'].includes(request.destination),
              handler: 'StaleWhileRevalidate',
              options: {
                cacheName: 'static-resources',
              },
            },
            {
              urlPattern: ({ request }) =>
                ['image', 'font'].includes(request.destination),
              handler: 'CacheFirst',
              options: {
                cacheName: 'asset-cache',
                expiration: {
                  maxEntries: 50,
                  maxAgeSeconds: 30 * 24 * 60 * 60,
                },
              },
            },
          ],
        },
      })
  ],
})
