import { defineStore } from 'pinia'
import api from '@/services/api'

export const useFriendsStore = defineStore('friends', {
  state: () => ({
    friends: []
  }),

  actions: {
    async loadFriends() {
      const response = await api.get('/friends')
      this.friends = response.data
    }
  }
})