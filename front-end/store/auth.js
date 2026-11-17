import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) =>
      typeof window !== 'undefined' ? !!localStorage.getItem('token') : false,
  },
  actions: {
    setToken(newToken) {
      this.token = newToken;
      if (typeof window !== 'undefined') {
        localStorage.setItem('token', newToken);
      }
    },
    setUserName(newName) {
      this.name = newName;
      if (typeof window !== 'undefined') {
        localStorage.setItem('userName', newName);
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
    },
    getToken() {
      if (typeof window !== 'undefined') {
        return localStorage.getItem('token');
      }
      return null;
    },
    getName() {
      if (typeof window !== 'undefined') {
        return localStorage.getItem('userName');
      }
      return null;
    },
  },
});
