import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {

  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false
  }),

/* =========================
   GETTERS
========================= */

  getters: {
    isAuthenticated: (state) => !!state.token
  },

/* =========================
   ACTIONS
========================= */

  actions: {

    async login(credentials) {

      this.loading = true

      try {

        const res = await api.post('/auth/login', credentials)

        this.token = res.data.access_token
        this.user = res.data.user

        localStorage.setItem('token', this.token)

      } finally {
        this.loading = false
      }
    },

    async signup(data) {
      await api.post('/auth/signup', data)
    },

    async fetchUser() {

      if (!this.token) return

      const res = await api.get('/auth/me')

      this.user = res.data
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }

  }

})