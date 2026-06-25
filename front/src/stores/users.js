import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUsersStore = defineStore('users', {

  state: () => ({
    users: [],
    selectedUser: null,
    loading: false
  }),

  getters: {

    userCount: (state) =>
      state.users.length,

    getUserById: (state) => {
      return (id) =>
        state.users.find(
          user => user.id === id
        )
    }

  },

  actions: {

    async loadUsers() {

      this.loading = true

      try {

        const response =
          await api.get('/users')

        this.users =
          response.data

      } finally {

        this.loading = false

      }
    },

    async loadUser(id) {

      const response =
        await api.get(
          `/users/${id}`
        )

      this.selectedUser =
        response.data
    },

    async searchUsers(query) {

      const response =
        await api.get(
          `/users/search?q=${query}`
        )

      return response.data
    },

    async deleteUser(id) {

      await api.delete(
        `/users/${id}`
      )

      this.users =
        this.users.filter(
          user => user.id !== id
        )
    }

  }

})