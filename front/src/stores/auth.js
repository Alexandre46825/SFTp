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
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_admin === true
    //isAdmin: true
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
        localStorage.setItem('token', this.token)

        await this.fetchUser()

        return res.data

      } finally {
        this.loading = false
      }
    },

    async signup(data) {
      await api.post('/auth/register', data)
    },

    async fetchUser() {

      if (!this.token) return

      try {
        const res = await api.get('/users/me')
        this.user = res.data
      } catch (err) {
        console.error("fetchUser failed", err)
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')

      delete api.defaults.headers.common['Authorization']
    },

    async updateProfile(data) {
      const res = await api.put('/users/me/update', data)
      this.user = res.data
    },

    async changePassword(data) {
      return await api.put('/users/me/password', data)
    }

  }

})