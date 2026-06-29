import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAdminUsersStore = defineStore('adminUsers', {
  state: () => ({
    users: [],
    selectedUser: null,
    loading: false
  }),

  actions: {

    /* =========================
       GET ALL USERS
    ========================= */
    async fetchUsers() {
      this.loading = true
      try {
        const res = await api.get('/admin/users')
        this.users = res.data
      } finally {
        this.loading = false
      }
    },

    /* =========================
       GET ONE USER (optionnel si API dispo)
    ========================= */
    async fetchUserById(id) {
      const res = await api.get(`/users/${id}`)
      this.selectedUser = res.data
    },

    /* =========================
       BAN / UNBAN
    ========================= */
    async banUser(id, data) {
      await api.put(`/admin/users/${id}/ban`, data)
      await this.fetchUsers()
    },

    async unbanUser(id) {
      await api.put(`/admin/users/${id}/unban`)
      await this.fetchUsers()
    },

    /* =========================
       ROLE UPDATE
    ========================= */
    async updateRole(id, role) {
      const res = await api.put(`/admin/users/${id}/role`, {
        is_admin: role
      })
      await this.fetchUsers()
      return res
    },

    /* =========================
       DELETE USER
    ========================= */
    async deleteUser(id) {
      await api.delete(`/admin/users/${id}`)
      await this.fetchUsers()
    }
  }
})