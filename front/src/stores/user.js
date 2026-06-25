import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null
  }),

  actions: {
    async loadProfile() {
      const response = await api.get(
        '/users/me'
      )

      this.profile = response.data
    },

    async updateProfile(data) {
      const response = await api.put(
        '/users/me',
        data
      )

      this.profile = response.data
    }
  }
})