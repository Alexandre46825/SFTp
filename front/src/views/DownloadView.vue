<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useFilesStore } from '@/stores/files'
import { useModalStore } from '@/stores/modal'
import api from '@/services/api'

const route = useRoute()
const filesStore = useFilesStore()
const modal = useModalStore()

/* =========================
   LOAD
========================= */
onMounted(async () => {
  await filesStore.loadFiles()
})

/* =========================
   FILE
========================= */
const file = computed(() => {
  return filesStore.files.find(
    f => f.id_file === Number(route.params.id_file)
  )
})

console.log(file.value)

/* =========================
   UI
========================= */
const decryptionPassword = ref('')
const downloading = ref(false)
const progress = ref(0)

let interval = null

/* =========================
   DOWNLOAD
========================= */
async function downloadFile() {
  if (!file.value) return

  downloading.value = true
  progress.value = 0

  // simulation UI
  interval = setInterval(() => {
    if (progress.value >= 90) {
      clearInterval(interval)
      return
    }
    progress.value += 10
  }, 120)

  try {
    // ⚠️ API download réelle
    const res = await api.get(`/files/download/${file.value.id_file}`, {
      params: {
        password_pgp : decryptionPassword.value
      }
    })

    clearInterval(interval)
    progress.value = 100

    // download browser
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')

    link.href = url
    link.setAttribute('download', file.value.file_name)
    document.body.appendChild(link)
    link.click()

    link.remove()

    modal.success(
      'Download Complete',
      'The file has been successfully downloaded.'
    )

  } catch (e) {
    console.error(e)
    modal.error(
      'Error',
      'An error occurred while trying to download the file. Please check the decryption password and try again.'
    )
  } finally {
    downloading.value = false
  }
}
</script>

<template>
  <div class="p-6 space-y-8">

    <h1 class="text-3xl font-bold mb-8">
      Download file
    </h1>

    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-8 space-y-8">

      <div class="flex items-center gap-5">

        <div class="text-6xl">
          📦
        </div>

        <div>

          <h2 class="text-2xl font-bold">
            {{ file.file_name }}
          </h2>

          <p class="text-slate-400">
            {{ file.size }}
          </p>

        </div>

      </div>

      <div class="grid md:grid-cols-2 gap-6">

        <div>
          <p class="text-slate-400 text-sm">
            Sender
          </p>

          <p class="font-semibold">
            {{ file.sender.username }}
          </p>
        </div>
        
        <div>
          <p class="text-slate-400 text-sm">
            Message
          </p>

          <p class="font-semibold">
            {{ file.message}}
          </p>
        </div>
        
        <div>
          <p class="text-slate-400 text-sm">
            Upload date
          </p>

          <p class="font-semibold">
            {{ new Date(file.upload_at).toLocaleString('fr-FR') }}
          </p>
        </div>

        <div>
          <p class="text-slate-400 text-sm">
            Expires
          </p>

          <p class="font-semibold">
            {{ new Date(file.expires_at).toLocaleString('fr-FR') }}
          </p>
        </div>


      </div>

      <div>

        <label class="block mb-2 font-medium">
          Decryption password
        </label>

        <input
          v-model="decryptionPassword"
          type="password"
          placeholder="Enter the encryption password..."
          class="w-full rounded-xl bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-4"
        >

      </div>

      <button
        class="w-full bg-green-600 hover:bg-green-700 rounded-xl py-4 text-lg font-semibold transition"
        @click="downloadFile"
        :disabled="downloading"
      >
        📥 Download file
      </button>

      <div v-if="downloading">

        <div class="flex justify-between mb-2 text-sm">

          <span>
            Downloading...
          </span>

          <span>
            {{ progress }}%
          </span>

        </div>

        <div class="w-full h-3 rounded-full bg-slate-700 overflow-hidden">

          <div
            class="h-full bg-green-500 transition-all"
            :style="{ width: progress + '%' }"
          />

        </div>

      </div>

    </div>

  </div>
</template>