<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFriendsStore } from '@/stores/friends'
import { useUsersStore } from '@/stores/users'
import {useModalStore} from '@/stores/modal'
import api from '@/services/api'

/* =========================
   LOAD DATA
========================= */
const modal = useModalStore()
const friendsStore = useFriendsStore()

const friends = computed(() => friendsStore.friends)
const usersStore = useUsersStore()

onMounted(async () => {
  await friendsStore.refreshAll()
  if (usersStore.users.length === 0) {
    await usersStore.loadUsers()
  }
})

/* =========================
   FILE
========================= */

const selectedFile = ref(null)
const fileInput = ref(null)

function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  selectedFile.value = file
}

function removeFile() {
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}

/* =========================
   FORM
========================= */
const message = ref('')
const expiration = ref('7') // jours
const uploadProgress = ref(0)

let interval = null

function startUpload() {
  uploadFile()
}

/* =========================
   RECIPIENTS
   -> on stocke uniquement des ID
========================= */
const recipients = ref([])
const selectedRecipient = ref('')

function addRecipient() {
  if (!selectedRecipient.value) return

  const id = parseInt(selectedRecipient.value)

  if (!recipients.value.includes(id)) {
    recipients.value.push(id)
  }

  selectedRecipient.value = ''
}

function removeRecipient(id) {
  recipients.value = recipients.value.filter(r => r !== id)
}

/* =========================
   API UPLOAD
========================= */
async function uploadFile() {
  if (!selectedFile.value || recipients.value.length === 0){
    modal.error(
      'Error',
      'Please select a file and at least one recipient before uploading.'
    )
    return
  }

  const formData = new FormData()

  formData.append('file', selectedFile.value)

  // backend attend un user_id → on envoie 1 fichier = 1 user
  // donc on boucle ou on envoie plusieurs requêtes
  const promises = recipients.value.map(userId => {
    const fd = new FormData()
    fd.append('file', selectedFile.value)
    fd.append('user_id', userId)
    fd.append('expiration_date', expiration.value)
    fd.append('message', message.value)

    return api.post('/files/send', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  })

  uploadProgress.value = 0

  interval = setInterval(() => {
    if (uploadProgress.value >= 100) {
      clearInterval(interval)
      return
    }
    uploadProgress.value += 10
  }, 200)

  try {
    await Promise.all(promises)
    uploadProgress.value = 100
    modal.success(
      'Upload Complete',
      'The file has been successfully uploaded and sent to the selected recipients.'
    )
  } catch (e) {
    console.error(e)
    clearInterval(interval)
    modal.error(
      'Error',
      'An error occurred while trying to upload the file.'
    )
  }
}
</script>

<template>
  <div class="p-6 space-y-8">
    
    <div>
      <h1 class="text-3xl font-bold">Send a file</h1>
      <p class="text-slate-400">Share files with your contacts</p>
    </div>

    <div class="bg-white dark:bg-gray-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-8 space-y-8">

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

        <div class="flex items-center justify-between bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
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
        <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700">

          <label class="block text-sm font-medium text-slate-400 mb-3">
            Recipient
          </label>

          <div class="flex flex-wrap gap-2 mb-3">
            <span
              v-for="id in recipients"
              :key="id"
              class="bg-blue-600/20 text-blue-300 px-4 py-2 rounded-full flex items-center gap-2"
            >
              {{ usersStore.users.find(u => u.id_user === id)?.username }}

              <button @click="removeRecipient(id)">✕</button>
            </span>

            <div class="flex gap-2">
              <select
                v-model="selectedRecipient"
                class="rounded-full border border-slate-600 px-4 py-2 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700"
              >
                <option value="">
                  Select a friend
                </option>

                <option
                  v-for="friend in friends"
                  :key="friend.id_user"
                  :value="friend.id_user"
                >
                  {{ friend.username || 'Unknown' }}
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
        <div class="p-4 rounded-xl border border-slate-200 dark:border-slate-700">
          <label class="block text-sm font-medium text-slate-400 mb-3">
            Expires in
          </label>

          <select
            v-model="expiration"
            class="w-full rounded-xl bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-blue-500 outline-none"
          >
            <option value="1">1 day</option>
            <option value="3">3 days</option>
            <option value="7">7 days</option>
            <option value="30">30 days</option>
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
          class="w-full rounded-xl bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-4 outline-none focus:border-blue-500 resize-none"
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
      <div v-if="uploadProgress > 0" class="space-y-3">
        <div class="flex justify-between text-sm">
          <span class="text-slate-300">
              {{ uploadProgress < 100 ? 'Uploading...' : 'Upload complete!' }}
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
          {{ (uploadProgress / 100 * selectedFile.size).toFixed(2) }} MB uploaded
        </p>
      </div>
    </div>
  </div>
</template>