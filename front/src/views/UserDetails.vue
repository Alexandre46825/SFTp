<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminUsersStore } from '@/stores/adminUsers'
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()

const route = useRoute()
const adminUsers = useAdminUsersStore()
const selectedRole = ref(0)

const user = ref(null)


onMounted(async () => {
  await adminUsers.fetchUserById(route.params.id)
  user.value = adminUsers.selectedUser
  selectedRole.value = user.value.is_admin
})

async function changeRole(role) {
  const res = await adminUsers.updateRole(user.value.id_user, role)
  
  if (res) {
    modal.success(
      'Role Updated',
      'The user role has been successfully updated.'
    )
  } else {
    modal.error(
      'Error',
      'An error occurred while updating the role.'
    )
  }
  user.value.role = role
}

async function deleteUser() {
  await adminUsers.deleteUser(user.value.id_user)
}

const showBanModal = ref(false)

const banReason = ref('')
const banDuration = ref('7d')

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

  user.value.account_status = 0
  showBanModal.value = false
}

async function toggleBan() {
  if (user.value.account_status == 2) {
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
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

      <!-- LOCATION -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <p class="text-xs text-slate-400 mb-1">📍 Location</p>
        <p class="font-medium">{{ user.location }}</p>
      </div>

      <!-- LAST LOGIN -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <p class="text-xs text-slate-400 mb-1">🕒 Last login</p>
        <p class="font-medium">{{ new Date(user.last_login).toLocaleString('fr-FR') || 'Unknown' }}</p>
      </div>

      <!-- ROLE -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <p class="text-xs text-slate-400 mb-2">🎭 Role</p>

        <select
          v-model="selectedRole"
          @change="changeRole(selectedRole)"
          class="w-full bg-slate-800 text-white border border-slate-600 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="false">User</option>
          <option :value="true">Admin</option>
        </select>
      </div>

      <!-- STATUS -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <p class="text-xs text-slate-400 mb-1">🚦 Status</p>

        <span
          class="inline-block px-3 py-1 rounded-full text-xs font-medium"
          :class="user.account_status === 1
            ? 'bg-green-500/20 text-green-400'
            : 'bg-red-500/20 text-red-400'"
        >
          {{ user.account_status == 0 ? 'Banned' : (user.account_status == 1 ? 'Active' : 'Deleted') }}
        </span>
      </div>

    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- FRIENDS -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <h2 class="font-semibold mb-3">👥 Friends</h2>

        <div v-if="!user.friends?.length" class="text-slate-400 text-sm">
          No friends
        </div>

        <div class="space-y-2">
          <div
            v-for="f in user.friends"
            :key="f"
            class="p-2 bg-slate-800 rounded"
          >
            {{ f }}
          </div>
        </div>
      </div>

      <!-- LOGS -->
      <div class="p-4 bg-slate-900 rounded-xl border border-slate-700">
        <h2 class="font-semibold mb-3">📜 Activity logs</h2>

        <div v-if="!user.logs?.length" class="text-slate-400 text-sm">
          No logs available
        </div>

        <div class="space-y-2 text-sm">
          <div
            v-for="log in user.logs"
            :key="log.id"
            class="flex justify-between bg-slate-800 p-2 rounded"
          >
            <span>{{ log.text }}</span>
            <span class="text-slate-400">{{ log.time }}</span>
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
    class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-lg p-6"
    @click.stop
  >

    <div class="flex justify-between items-center mb-6">

      <h2 class="text-2xl font-bold">
        🚫 Ban user
      </h2>

      <button
        @click="closeBanModal"
        class="text-slate-400 hover:text-white"
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
        class="w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 resize-none"
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
        class="px-5 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white"
      >
        Confirm ban
      </button>

    </div>

  </div>

</div>
  
</template>