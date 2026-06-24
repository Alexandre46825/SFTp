// stores/friends.js

import { defineStore } from 'pinia'
import axios from 'axios'

export const useFriendsStore = defineStore('friends', {
  state: () => ({
    friends: []
  }),

  actions: {
    async loadFriends() {
      const response = await axios.get('/api/friends')
      this.friends = response.data
    }
  }
})