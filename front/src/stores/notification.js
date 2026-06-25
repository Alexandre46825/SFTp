import { defineStore } from 'pinia'
import api from '@/services/api'

export const useNotificationsStore =
defineStore('notifications', {

  state: () => ({
    notifications: []
  }),

  getters: {
    unreadCount: (state) =>
      state.notifications.filter(
        n => !n.read
      ).length
  },

  actions: {
    async loadNotifications() {
      const response =
        await api.get(
          '/notifications'
        )

      this.notifications =
        response.data
    },

    async markAsRead(id) {
      await api.put(
        `/notifications/${id}/read`
      )

      const notification =
        this.notifications.find(
          n => n.id === id
        )

      if (notification) {
        notification.read = true
      }
    }
  }
})