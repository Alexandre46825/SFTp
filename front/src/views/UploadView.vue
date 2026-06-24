<script setup>
import { ref, computed } from 'vue'
//import { useFriendsStore } from '@/stores/friends'

// Initialisation of the form data
const selectedFile = ref(null)
const fileInput = ref(null)

function handleFileChange(event) {
  const file = event.target.files[0]

  if (!file) return

  selectedFile.value = {
    file,
    name: file.name,
    size: +(file.size / 1024 / 1024).toFixed(2)
  }

  uploadProgress.value = 0
}

function removeFile() {
  selectedFile.value = null

  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const message = ref(
  'Here is the latest build — please review before Friday.'
)

const expiration = ref('7 days')
const uploadProgress = ref(65)

const uploadedSize = computed(() => {
  if (!selectedFile.value) return 0

  return (
    selectedFile.value.size * uploadProgress.value / 100
  ).toFixed(1)
})

const remainingTime = computed(() => {
  if (uploadProgress.value === 0 || !selectedFile.value) {
    return '--'
  }

  const speed = 5 // MB/s simulés

  const remaining =
    selectedFile.value.size - Number(uploadedSize.value)

  return Math.ceil(remaining / speed)
})
let interval = null

function startUpload() {
  if (!selectedFile.value) return

  uploadProgress.value = 0

  clearInterval(interval)

  interval = setInterval(() => {
    if (uploadProgress.value >= 100) {
      clearInterval(interval)
      return
    }

    uploadProgress.value += 5
  }, 500)
}
//const friendsStore = useFriendsStore()

const recipients = ref([])
const selectedRecipient = ref('')

function addRecipient() {
  if (
    selectedRecipient.value &&
    !recipients.value.includes(selectedRecipient.value)
  ) {
    recipients.value.push(selectedRecipient.value)
  }

  selectedRecipient.value = ''
}
function removeRecipient(recipient) {
  recipients.value = recipients.value.filter(
    r => r !== recipient
  )
}
// const formData = new FormData()
// formData.append('file', selectedFile.value.file)

// await axios.post('/api/upload', formData, {
//   onUploadProgress: (event) => {
//     uploadProgress.value = Math.round(
//       (event.loaded * 100) / event.total
//     )
//   }
// })
</script>

<template>
  <div class="p-6 space-y-8">
    
    <div>
      <h1 class="text-3xl font-bold">Send a file</h1>
      <p class="text-slate-400">Share files with your contacts</p>
    </div>

    <div class="bg-white dark:bg-gray-800 border border-slate-700 rounded-2xl p-8 space-y-8">

      <!-- Browse files -->
      <div>
        <label class="block text-sm font-medium text-slate-400 mb-3">
          Browse files
        </label>

        <label
          class="flex items-center justify-center w-full h-36 border-2 border-dashed border-slate-600 rounded-xl cursor-pointer hover:border-blue-500 transition"
        >
          <div class="text-center">
            <p class="text-lg font-medium">
              📁 Choose a file
            </p>

            <p class="text-sm text-slate-400 mt-1">
              Click or drag and drop your file
            </p>
          </div>

          <input
            ref="fileInput"
            type="file"
            class="hidden"
            @change="handleFileChange"
          />
        </label>
      </div>

      <!-- Selected file -->
      <div v-if="selectedFile">
        <label class="block text-sm font-medium text-slate-400 mb-3">
          Selected file
        </label>

        <div class="flex items-center justify-between bg-slate-900 rounded-xl p-4 border border-slate-700">
          <div class="flex items-center gap-4">
            <div class="text-3xl">
              📦
            </div>

            <div>
              <p class="font-medium">
                {{ selectedFile.name }}
              </p>

              <p class="text-sm text-slate-400">
                {{ selectedFile.size }} MB
              </p>
            </div>
          </div>

          <button
            class="text-red-400 hover:text-red-300"
            @click="removeFile"
          >
            Delete
          </button>
        </div>
      </div>

      <!-- Recipient -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
        <div class="p-4 rounded-xl border border-slate-700">

          <label class="block text-sm font-medium text-slate-400 mb-3">
            Recipient
          </label>

          <div class="flex flex-wrap gap-2 mb-3">
            <span
              v-for="recipient in recipients"
              :key="recipient"
              class="bg-blue-600/20 text-blue-300 px-4 py-2 rounded-full flex items-center gap-2"
            >
              {{ recipient }}

              <button @click="removeRecipient(recipient)">
                ✕
              </button>
            </span>

            <div class="flex gap-2">
              <select
                v-model="selectedRecipient"
                class="rounded-full border border-slate-600 px-4 py-2 bg-slate-900"
              >
                <option value="">
                  Select a friend
                </option>

                <option
                  v-for="friend in friends"
                  :key="friend"
                  :value="friend"
                >
                  {{ friend }}
                </option>
              </select>

              <button
                class="px-4 py-2 rounded-full border border-slate-600"
                @click="addRecipient"
              >
                Add
              </button>
            </div>
          </div>
        </div>
        <div class="p-4 rounded-xl border border-slate-700">
          <label class="block text-sm font-medium text-slate-400 mb-3">
            Expires in
          </label>

          <select
            v-model="expiration"
            class="w-full rounded-xl bg-slate-900 border border-slate-700 p-3 focus:border-blue-500 outline-none"
          >
            <option>1 day</option>
            <option>3 days</option>
            <option>7 days</option>
            <option>30 days</option>
          </select>
        </div>
      </div>

      <!-- Message -->
      <div>
        <label class="block text-sm font-medium text-slate-400 mb-3">
          Message (optional)
        </label>

        <textarea
          v-model="message"
          rows="4"
          class="w-full rounded-xl bg-slate-900 border border-slate-700 p-4 outline-none focus:border-blue-500 resize-none"
        />
      </div>
      <!-- Send button -->
      <button
        class="w-full bg-blue-600 hover:bg-blue-700 transition rounded-xl py-4 font-semibold text-lg"
        @click="startUpload"
      >
        🔒 Send securely
      </button>

      <!-- Upload progress -->
      <div class="space-y-3">
        <div class="flex justify-between text-sm">
          <span class="text-slate-300">
            Upload in progress…
          </span>

          <span class="text-slate-400">
            {{ uploadProgress }}%
          </span>
        </div>

        <div class="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
          <div
            class="h-full bg-blue-500 transition-all duration-500"
            :style="{ width: `${uploadProgress}%` }"
          />
        </div>

        <p
          v-if="selectedFile"
          class="text-sm text-slate-400"
        >
          {{ uploadedSize }} MB of {{ selectedFile.size }} MB · ~{{ remainingTime }}s remaining
        </p>
      </div>
    </div>
  </div>
</template>