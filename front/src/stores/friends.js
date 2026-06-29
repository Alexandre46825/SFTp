import { defineStore } from 'pinia'
import api from '@/services/api'

export const useFriendsStore = defineStore('friends', {
  state: () => ({
    friends: [],
    requests: [],
    suggestions: [],
    loading: false
  }),

  actions: {

    async loadFriends() {
      this.loading = true
      try {
        const res = await api.get('/friends/list')
        
        this.friends = res.data
      } finally {
        this.loading = false
      }
    },

    async loadRequests() {
      const res = await api.get('/friends/requests')
      this.requests = res.data
    },

    async addFriend(friendId) {
      await api.post('/friends/add', {
        id_receiver: friendId
      })
    },

    async acceptFriend(friendshipId) {
      await api.put(`/friends/accept/${friendshipId}`)
      await this.refreshAll()
    },

    async blockFriend(friendshipId) {
      await api.put(`/friends/block/${friendshipId}`)
      await this.refreshAll()
    },

    async removeFriend(friendshipId) {
      await api.delete(`/friends/remove/${friendshipId}`)
      await this.refreshAll()
    },

    async refreshAll() {
      await Promise.all([
        this.loadFriends(),
        this.loadRequests()
      ])
    }
  }
})