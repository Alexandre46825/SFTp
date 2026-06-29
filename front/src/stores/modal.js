import { defineStore } from 'pinia'

export const useModalStore = defineStore('modal', {
  state: () => ({
    show: false,
    title: '',
    message: '',
    type: 'info', // success | error | info
    button: 'OK'
  }),

  actions: {
    success(title, message) {
      this.title = title
      this.message = message
      this.type = 'success'
      this.show = true
    },

    error(title, message) {
      this.title = title
      this.message = message
      this.type = 'error'
      this.show = true
    },

    info(title, message) {
      this.title = title
      this.message = message
      this.type = 'info'
      this.show = true
    },

    close() {
      this.show = false
    }
  }
})