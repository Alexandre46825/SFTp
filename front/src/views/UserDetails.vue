<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminUsersStore } from '@/stores/adminUsers'
import { useModalStore } from '@/stores/modal'
import api from '@/services/api'

const modal = useModalStore()
const route = useRoute()
const adminUsers = useAdminUsersStore()

const user = ref(null)
const logs = ref([])
const friends = ref([])


const selectedRole = ref(false)

const showBanModal = ref(false)
const banReason = ref('')
const banDuration = ref('7d')

/* =========================
   LOAD USER + EXTRA DATA
========================= */
onMounted(async () => {
  await adminUsers.fetchUserById(route.params.id)
  user.value = adminUsers.selectedUser

  selectedRole.value = user.value.is_admin

  await Promise.all([
    fetchLogs(),
    fetchFriends()
  ])
})

/* =========================
   LOGS
========================= */
async function fetchLogs() {
  try {
    const res = await api.get(`/admin/logs/${route.params.id}`)
    logs.value = res.data
  } catch (e) {
    console.error('Logs error:', e)
  }
}

/* =========================
   FRIENDS
========================= */
async function fetchFriends() {
  try {
    const res = await api.get(`/friends/list/${route.params.id}`)
    friends.value = res.data
  } catch (e) {
    console.error('Friends error:', e)
  }
}

/* =========================
   ROLE
========================= */
async function changeRole(role) {
  const res = await adminUsers.updateRole(user.value.id_user, role)

  if (res) {
    modal.success('Role updated', 'User role updated successfully')
    user.value.is_admin = role
  } else {
    modal.error('Error', 'Failed to update role')
  }
}

/* =========================
   DELETE USER (FIXED BUG)
========================= */
async function deleteUser() {
  const res = await adminUsers.deleteUser(user.value.id_user)

  if (res) {
    user.value.account_status = 3
    modal.success('Deleted', 'User marked as deleted')
  }
}

/* =========================
   STATUS HELPERS
========================= */
const statusLabel = (status) => {
  switch (status) {
    case 1: return 'Active'
    case 2: return 'Banned'
    case 3: return 'Deleted'
    default: return 'Unknown'
  }
}

const statusColor = (status) => {
  switch (status) {
    case 1: return 'bg-green-500/20 text-green-400'
    case 2: return 'bg-yellow-500/20 text-yellow-400'
    case 3: return 'bg-red-500/20 text-red-400'
    default: return 'bg-slate-500/20 text-slate-400'
  }
}

/* =========================
   BAN SYSTEM
========================= */
function openBanModal() {
  banReason.value = ''
  banDuration.value = '7d'
  showBanModal.value = true
}

function closeBanModal() {
  showBanModal.value = false
}

async function confirmBan() {
  await adminUsers.banUser(user.value.id_user, {
    reason: banReason.value
  })

  user.value.account_status = 2
  showBanModal.value = false
}

async function toggleBan() {
  if (user.value.account_status === 2) {
    await adminUsers.unbanUser(user.value.id_user)
    user.value.account_status = 1
  } else {
    openBanModal()
  }
}
</script>

<template>
  <div v-if="user" class="p-6 space-y-8">

    <!-- HEADER -->
    <div class="flex justify-between items-start">
      <div>
        <h1 class="text-3xl font-bold">
          {{ user.name }} {{ user.surname }}
        </h1>
        <p class="text-slate-400">{{ user.mail }}</p>
      </div>

      <div class="flex gap-2">
        <button
          @click="toggleBan"
          class="px-4 py-2 rounded bg-yellow-600/20 text-yellow-400 hover:bg-yellow-600/30 transition"
        >
          {{ user.account_status == 2 ? 'Unban user' : 'Ban user' }}
        </button>

        <button
          v-if="user.account_status === 1"
          @click="deleteUser"
          class="px-4 py-2 rounded bg-red-600/20 text-red-400 hover:bg-red-600/30 transition"
        >
          Delete user
        </button>
      </div>
    </div>

    <!-- INFOS GRID -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

      <!-- LOCATION -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-xs text-slate-400 mb-1">📍 Location</p>
        <p class="font-medium">{{ user.location }}</p>
      </div>

      <!-- LAST LOGIN -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-xs text-slate-400 mb-1">🕒 Last login</p>
        <p class="font-medium">{{ new Date(user.last_login).toLocaleString('fr-FR') || 'Unknown' }}</p>
      </div>

      
      <!-- FILE SIZE -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-xs text-slate-400 mb-1">📁 File size</p>
        <p class="font-medium">{{ user.file_size }} MB</p>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
      <!-- ROLE -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-xs text-slate-400 mb-2">🎭 Role</p>

        <select
          v-model="selectedRole"
          @change="changeRole(selectedRole)"
          class="w-full bg-slate-800 text-slate-900 dark:text-white border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="false">User</option>
          <option :value="true">Admin</option>
        </select>
      </div>

      <!-- STATUS -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <p class="text-xs text-slate-400 mb-1">🚦 Status</p>

        <span
          class="inline-block px-3 py-1 rounded-full text-xs font-medium"
          :class="statusColor(user.account_status)"
        >
          {{ statusLabel(user.account_status) }}
        </span>
      </div>

    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- FRIENDS -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <h2 class="font-semibold mb-3">👥 Friends</h2>

        <div v-if="!friends?.length" class="text-slate-400 text-sm">
          No friends
        </div>

        <div class="space-y-2">
          <div v-for="f in friends" :key="f.id_user" class="p-2 bg-slate-800 rounded">
            <p class="font-medium">{{ f.username }}</p>
            <p class="text-xs text-slate-400">{{ f.mail }}</p>
          </div>
        </div>
      </div>

      <!-- LOGS -->
      <div class="p-4 bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl border border-slate-200 dark:border-slate-700">
        <h2 class="font-semibold mb-3">📜 Activity logs</h2>

        <div v-if="!logs.length" class="text-slate-400 text-sm">
          No logs available
        </div>

        <div class="space-y-2 text-sm">
          <div v-for="log in logs" :key="log.id_log" class="flex justify-between bg-slate-800 p-2 rounded">
            <span>{{ log.action_type }}</span>
            <span class="text-slate-400">
              {{ new Date(log.log_timestamp).toLocaleString() }}
            </span>
          </div>
        </div>
      </div>

    </div>

  </div>
  <!-- ================= BAN MODAL ================= -->
<div
  v-if="showBanModal"
  class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
  @click="closeBanModal"
>

  <div
    class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 w-full max-w-lg p-6"
    @click.stop
  >

    <div class="flex justify-between items-center mb-6">

      <h2 class="text-2xl font-bold">
        🚫 Ban user
      </h2>

      <button
        @click="closeBanModal"
        class="text-slate-400 hover:text-slate-900 dark:text-white"
      >
        ✕
      </button>

    </div>

    <!-- Reason -->
    <div>

      <label class="block text-sm text-slate-400 mb-2">
        Reason
      </label>

      <textarea
        v-model="banReason"
        rows="5"
        placeholder="Explain why this user is banned..."
        class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 px-3 py-2 resize-none"
      />

    </div>

    <!-- Buttons -->
    <div class="flex justify-end gap-3 mt-6">

      <button
        @click="closeBanModal"
        class="px-5 py-2 rounded-lg border border-slate-600 hover:bg-slate-700"
      >
        Cancel
      </button>

      <button
        @click="confirmBan"
        class="px-5 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-slate-900 dark:text-white"
      >
        Confirm ban
      </button>

    </div>

  </div>

</div>
  
</template>