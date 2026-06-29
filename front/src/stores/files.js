import { defineStore } from 'pinia'
import api from '@/services/api'

export const useFilesStore = defineStore('files', {

  state: () => ({
    files: [],
    selectedFile: null,
    uploadProgress: 0,
    loading: false
  }),

  getters: {

    totalFiles: (state) => state.files.length,

    totalSize: (state) =>
      state.files.reduce(
        (sum, file) => sum + (file.file_size || 0),
        0
      ),

    recentFiles: (state) =>
      [...state.files]
        .sort((a, b) =>
          new Date(b.upload_at) - new Date(a.upload_at)
        )
        .slice(0, 5)
  },

  actions: {

    async loadFiles() {
      this.loading = true
      try {
        const res = await api.get('/files/my-files')

        this.files = res.data.map(file => ({
          ...file,
          name: file.file_name,
          size: file.file_size,
          uploaded_at: file.upload_at,
          expires_at: file.expires_at
        }))

      } finally {
        this.loading = false
      }
    },

    selectFile(file) {
      this.selectedFile = file
    },

    clearSelectedFile() {
      this.selectedFile = null
    },

    async uploadFile({
      file,
      message = '',
      expiration_date = 7,
      recipients = []
    }) {

      this.uploadProgress = 0

      const requests = recipients.map(userId => {
        const fd = new FormData()

        fd.append('file', file)
        fd.append('user_id', userId)
        fd.append('message', message)
        fd.append('expiration_date', expiration_date)

        return api.post('/files/send', fd, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      })

      await Promise.all(requests)

      await this.loadFiles()
      this.uploadProgress = 0
    },

    async downloadFile(fileId) {
      const res = await api.get(
        `/files/download/${fileId}`,
        { responseType: 'blob' }
      )

      const url = window.URL.createObjectURL(new Blob([res.data]))

      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'file')
      document.body.appendChild(link)
      link.click()
    }

  }
})