<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useUsersStore } from '@/stores/users'

const usersStore = useUsersStore()

const logs = ref([])
const loading = ref(false)

/* =========================
   LOAD LOGS
========================= */
async function loadLogs() {
  loading.value = true

  try {
    const res = await api.get('/admin/logs')
    logs.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadLogs()

  if (usersStore.users.length === 0) {
    await usersStore.loadUsers()
  }
})

/* =========================
   HELPERS
========================= */
function getUser(id) {
  return usersStore.users.find(u => u.id_user === id)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('fr-FR', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

function getActionType(action) {
  if (action.startsWith('file_downloaded')) return 'download'
  if (action.startsWith('file_sent')) return 'send'
  return 'other'
}
</script>

<template>
  <div class="p-6 space-y-6">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">System Logs</h1>
      <p class="text-slate-400">Activity tracking and audit trail</p>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-slate-400">
      Loading logs...
    </div>

    <!-- TABLE -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden">

      <table class="w-full text-left text-sm">
        <thead class="bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 text-slate-300">
          <tr>
            <th class="p-3">User</th>
            <th class="p-3">Action</th>
            <th class="p-3">IP</th>
            <th class="p-3">Date</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="log in logs"
            :key="log.id_log"
            class="border-t border-slate-200 dark:border-slate-700 hover:bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700/50 transition"
          >

            <!-- USER -->
            <td class="p-3">
              <div class="font-medium">
                {{ getUser(log.id_user)?.username || 'Unknown' }}
              </div>
              <div class="text-xs text-slate-400">
                ID: {{ log.id_user }}
              </div>
            </td>

            <!-- ACTION -->
            <td class="p-3">
              <span
                class="px-2 py-1 rounded-full text-xs font-semibold"
                :class="{
                  'bg-green-500/20 text-green-400': getActionType(log.action_type) === 'send',
                  'bg-blue-500/20 text-blue-400': getActionType(log.action_type) === 'download',
                  'bg-slate-500/20 text-slate-300': getActionType(log.action_type) === 'other'
                }"
              >
                {{ log.action_type }}
              </span>
            </td>

            <!-- IP -->
            <td class="p-3 text-slate-300">
              {{ log.ip_address }}
            </td>

            <!-- DATE -->
            <td class="p-3 text-slate-400">
              {{ formatDate(log.log_timestamp) }}
            </td>

          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>