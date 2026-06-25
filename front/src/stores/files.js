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
        (sum, file) => sum + (file.size || 0),
        0
      ),

    recentFiles: (state) =>
      [...state.files]
        .sort(
          (a, b) =>
            new Date(b.created_at) -
            new Date(a.created_at)
        )
        .slice(0, 5)
  },

  actions: {

    /* =========================
       LOAD FILES
    ========================= */
    async loadFiles() {

      this.loading = true

      try {

        const response =
          await api.get('/files')

        this.files = response.data

      } finally {
        this.loading = false
      }
    },

    /* =========================
       SELECT FILE (frontend)
    ========================= */
    selectFile(file) {
      this.selectedFile = file
    },

    clearSelectedFile() {
      this.selectedFile = null
    },

    /* =========================
       UPLOAD FILE
    ========================= */
    async uploadFile({
      file,
      message = '',
      expiration = '7 days',
      encryption = 'AES-256',
      recipients = []
    }) {

      const formData = new FormData()

      formData.append('file', file)
      formData.append('message', message)
      formData.append('expiration', expiration)
      formData.append('encryption', encryption)

      recipients.forEach(r =>
        formData.append('recipients[]', r)
      )

      this.uploadProgress = 0

      const response = await api.post(
        '/files/upload',
        formData,
        {
          headers: {
            'Content-Type':
              'multipart/form-data'
          },

          onUploadProgress: (event) => {

            this.uploadProgress =
              Math.round(
                (event.loaded * 100) /
                event.total
              )
          }
        }
      )

      await this.loadFiles()

      return response.data
    },

    /* =========================
       DELETE FILE
    ========================= */
    async deleteFile(fileId) {

      await api.delete(
        `/files/${fileId}`
      )

      this.files =
        this.files.filter(
          f => f.id !== fileId
        )
    },

    /* =========================
       DOWNLOAD FILE
    ========================= */
    async downloadFile(fileId) {

      const response =
        await api.get(
          `/files/${fileId}/download`,
          {
            responseType: 'blob'
          }
        )

      const url =
        window.URL.createObjectURL(
          new Blob([response.data])
        )

      const link =
        document.createElement('a')

      link.href = url
      link.setAttribute(
        'download',
        'file'
      )

      document.body.appendChild(link)
      link.click()
    }

  }
})