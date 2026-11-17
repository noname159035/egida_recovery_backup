import axios from 'axios';

export default defineNuxtPlugin((nuxtApp) => {
  const apiBase = useRuntimeConfig().public.apiBase; // Доступ к переменной окружения для базового URL

  const instance = axios.create({
    baseURL: apiBase, // Используем путь `/api/` из конфигурации
    timeout: 5000,    // Таймаут запросов
  });

  // Добавляем экземпляр axios к Nuxt
  return {
    provide: {
      axios: instance, // Делаем $axios доступным в проекте
    },
  };
});
