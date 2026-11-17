export default defineNuxtConfig({
  // Заголовки страницы
  app: {
    head: {
      title: 'Secure LLM',
      htmlAttrs: {
        lang: 'ru',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: '' },
        { name: 'format-detection', content: 'telephone=no' },
      ],
      link: [{ rel: 'icon', href: '/favicon.ico' }],
    },
  },

  modules: [
    '@pinia/nuxt',
  ],

  // Глобальные стили
  css: [
    '@/static/css/global.css',
    '@/static/css/variables.css',
    '@/static/css/animations.css',
    '@/static/css/fonts.css',
  ],

  // Автоматическое импортирование компонентов
  components: true,

  runtimeConfig: {
    public: {
      apiUrl: process.env.PROXY_URL || 'http://127.0.0.1:8080',
    },
  },

  devtools: {
    enabled: true,
    inspector: false,
  },

  // Оптимизация Vite
  vite: {
    server: {
      watch: {
        ignored: ['**/node_modules/**', '**/.nuxt/**']
      }
    },
    build: {
      sourcemap: false
    }
  },

  build: {},

  compatibilityDate: '2025-02-22',
});
