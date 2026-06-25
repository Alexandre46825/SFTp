import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAdminStore = defineStore('admin', {

  state: () => ({
    users: [],
    selectedUser: null
  }),

  actions: {

    async loadUsers() {
      const response =
        await api.get(
          '/admin/users'
        )

      this.users = response.data
    },

    async loadUserDetails(id) {
      const response =
        await api.get(
          `/admin/users/${id}`
        )

      this.selectedUser =
        response.data
    },

    async banUser(id, duration) {
      await api.post(
        `/admin/users/${id}/ban`,
        {
          duration_days: duration
        }
      )

      await this.loadUsers()
    },

    async unbanUser(id) {
      await api.post(
        `/admin/users/${id}/unban`
      )

      await this.loadUsers()
    },

    async changeRole(id, role) {
      await api.put(
        `/admin/users/${id}/role`,
        {
          role
        }
      )

      await this.loadUsers()
    }
  }
})