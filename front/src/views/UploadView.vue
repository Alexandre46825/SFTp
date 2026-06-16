<script setup>
import { ref, computed } from 'vue'


// Initialisation of the form data
const selectedFile = ref({
  name: 'project_v2_final.tar.gz',
  size: 84,
})
const recipients = ref(['@marc', '@lea'])

const message = ref(
  'Here is the latest build — please review before Friday.'
)

const encryption = ref('AES-256')
const expiration = ref('7 days')

const uploadProgress = ref(65)

const uploadedSize = computed(() =>
  (selectedFile.value.size * uploadProgress.value / 100).toFixed(1)
)

const remainingTime = computed(() =>
  Math.round((selectedFile.value.size - uploadedSize.value) / (selectedFile.value.size / uploadProgress.value))
)
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <h2 class="text-3xl font-bold mb-8">
      Send a file
    </h2>

    <div class="bg-slate-800 border border-slate-700 rounded-2xl p-8 space-y-8">

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
            type="file"
            class="hidden"
          >
        </label>
      </div>

      <!-- Selected file -->
      <div>
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

          <button class="text-red-400 hover:text-red-300">
            Delete
          </button>
        </div>
      </div>

      <!-- Recipient -->
      <div>
        <label class="block text-sm font-medium text-slate-400 mb-3">
          Recipient
        </label>

        <div class="flex flex-wrap gap-2 mb-3">
          <span
            v-for="recipient in recipients"
            :key="recipient"
            class="bg-blue-600/20 text-blue-300 px-4 py-2 rounded-full"
          >
            {{ recipient }}
          </span>

          <button
            class="px-4 py-2 rounded-full border border-slate-600 hover:bg-slate-700 transition"
          >
            + Add recipient
          </button>
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

      <!-- Settings -->
      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-3">
            Encryption
          </label>

          <select
            v-model="encryption"
            class="w-full rounded-xl bg-slate-900 border border-slate-700 p-3 focus:border-blue-500 outline-none"
          >
            <option>AES-128</option>
            <option>AES-256</option>
          </select>
        </div>

        <div>
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

      <!-- Send button -->
      <button
        class="w-full bg-blue-600 hover:bg-blue-700 transition rounded-xl py-4 font-semibold text-lg"
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

        <p class="text-sm text-slate-400">
          {{ uploadedSize }} MB of {{ selectedFile.size }} MB · ~{{ remainingTime }}s remaining
        </p>
      </div>
    </div>
  </div>
</template>