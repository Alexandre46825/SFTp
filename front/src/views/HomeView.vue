<script setup>
import { onMounted, computed } from 'vue'

import StatCard from '@/components/StatCard.vue'

import { useUserStore } from '@/stores/user'
import { useFilesStore } from '@/stores/files'
import { useFriendsStore } from '@/stores/friends'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
const filesStore = useFilesStore()
const friendsStore = useFriendsStore()

onMounted(async () => {
  await Promise.all([
    userStore.loadProfile(),
    filesStore.loadFiles(),
    friendsStore.loadFriends()
  ])
})

/* =========================
   COMPUTED STATS
========================= */

const storageUsedGB = computed(() => {
  const totalBytes = filesStore.files.reduce(
    (sum, file) => sum + (file.size || 0),
    0
  )

  return (totalBytes / 1024 / 1024 / 1024).toFixed(2)
})

const filesCount = computed(() => filesStore.files.length)

const friendsCount = computed(
  () => friendsStore.friends.length
)

// Files:

const recentFiles = computed(() => {
  return filesStore.files
    .slice()
    .sort((a, b) => new Date(b.upload_at) - new Date(a.upload_at))
})

function openFile(file) {
  router.push(`/download/${file.id_file}`)
}
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">
        Welcome {{ userStore.profile?.username || 'User'}}
      </h1>

      <p class="text-slate-400">
        Here's what's happening with your account.
      </p>
    </div>

    <!-- STATS -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

      <StatCard
        title="Files sent"
        :value="`${filesCount}`"
      />

      <StatCard
        title="Storage used"
        :value="`${storageUsedGB} GB`"
      />

      <StatCard
        title="Friends"
        :value="`${friendsCount}`"
      />
      
      <StatCard
        title="Account role"
        :value="userStore.profile?.account_status == 1 ? 'User' : 'Administrator' || 'user'"
      />
    </div>

    <!-- QUICK INFO -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

      <StatCard
        title="Last login"
        :value="new Date(userStore.profile?.last_login).toLocaleString('fr-FR') || 'Unknown'"
      />

      <StatCard
        title="User email"
        :value="`${userStore.profile?.mail || 'Not loaded'}`"
      />

    </div>
    <!-- RECENT FILES -->
<div class="bg-white dark:bg-gray-800 border border-slate-700 rounded-2xl p-6">

  <h2 class="text-xl font-bold mb-4">
    📁 Recent files
  </h2>

  <div v-if="recentFiles.length === 0" class="text-slate-400 text-sm">
    No files uploaded yet
  </div>

  <div class="space-y-2">

    <div
      v-for="file in recentFiles"
      :key="file.id_file"
      @click="openFile(file)"
      class="flex items-center justify-between p-3 rounded-xl bg-slate-900 hover:bg-slate-800 cursor-pointer transition"
    >

      <!-- FILE INFO -->
      <div>
        <p class="font-medium">
          {{ file.file_name }}
        </p>

        <p class="text-xs text-slate-400">
          {{ file.file_size }} MB ·
          {{ new Date(file.upload_at).toLocaleDateString('fr-FR') }}
        </p>
      </div>

      <!-- SENDER -->
      <div class="text-right text-xs text-slate-400">
        <p>{{ file.sender.username }}</p>
        <p>{{ file.mime_type }}</p>
      </div>

    </div>

  </div>

</div>

  </div>
</template>