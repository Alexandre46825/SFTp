<script setup>
import { onMounted, computed } from 'vue'

import StatCard from '@/components/StatCard.vue'

import { useUserStore } from '@/stores/user'
import { useFilesStore } from '@/stores/files'
import { useNotificationsStore } from '@/stores/notification'
import { useFriendsStore } from '@/stores/friends'

const userStore = useUserStore()
const filesStore = useFilesStore()
const notificationsStore = useNotificationsStore()
const friendsStore = useFriendsStore()

onMounted(async () => {
  await Promise.all([
    userStore.loadProfile(),
    filesStore.loadFiles(),
    notificationsStore.loadNotifications(),
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

const notificationsCount = computed(
  () => notificationsStore.notifications.length
)

const unreadNotifications = computed(
  () => notificationsStore.unreadCount
)

const friendsCount = computed(
  () => friendsStore.friends.length
)
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">
        Welcome {{ userStore.profile?.firstname }}
      </h1>

      <p class="text-slate-400">
        Here's what's happening with your account.
      </p>
    </div>

    <!-- STATS -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

      <StatCard
        title="Files sent"
        :value="filesCount"
      />

      <StatCard
        title="Storage used"
        :value="`${storageUsedGB} GB`"
      />

      <StatCard
        title="Friends"
        :value="friendsCount"
      />

      <StatCard
        title="Notifications"
        :value="notificationsCount"
      />

    </div>

    <!-- SECOND ROW -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">

      <StatCard
        title="Unread notifications"
        :value="unreadNotifications"
      />

      <StatCard
        title="Account status"
        :value="userStore.profile?.role || 'user'"
      />

    </div>

    <!-- QUICK INFO -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

      <StatCard
        title="Last login"
        :value="userStore.profile?.last_login || 'Unknown'"
      />

      <StatCard
        title="User email"
        :value="userStore.profile?.email || 'Not loaded'"
      />

    </div>

  </div>
</template>