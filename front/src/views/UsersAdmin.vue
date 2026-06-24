<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* =========================
   SEARCH
========================= */
const search = ref('')

/* =========================
   USERS MOCK
========================= */
const users = ref([
  { id: 1, name: 'Marc', email: 'marc@mail.com', role: 'user', status: 'active' },
  { id: 2, name: 'Léa', email: 'lea@mail.com', role: 'admin', status: 'active' },
  { id: 3, name: 'Alex', email: 'alex@mail.com', role: 'user', status: 'banned' }
])

/* =========================
   FILTER
========================= */
const filteredUsers = computed(() => {
  return users.value.filter(u =>
    u.name.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase())
  )
})

/* =========================
   ACTIONS
========================= */

function openUser(user) {
  router.push(`/admin/users/${user.id}`)
}

function toggleBan(user) {
  user.status = user.status === 'banned' ? 'active' : 'banned'
}

function deleteUser(id) {
  users.value = users.value.filter(u => u.id !== id)
}

function changeRole(user, role) {
  user.role = role
}
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">Users management</h1>
      <p class="text-slate-400">Click a user to see full details</p>
    </div>

    <!-- SEARCH -->
    <input
      v-model="search"
      type="text"
      placeholder="Search user..."
      class="w-full md:w-1/3 p-3 rounded-xl bg-slate-900 border border-slate-700 outline-none focus:border-blue-500"
    />

    <!-- TABLE -->
    <div class="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
      <div class="overflow-x-auto"> 
      <table class="w-full text-sm min-w-[700px]">

        <thead class="bg-slate-800 text-slate-400 text-left">
          <tr>
            <th class="p-3">User</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="user in filteredUsers"
            :key="user.id"
            class="border-t border-slate-800 hover:bg-slate-800/40 transition"
          >

            <!-- CLICKABLE USER -->
            <td
              class="p-3 font-medium cursor-pointer hover:text-blue-400"
              @click="openUser(user)"
            >
              {{ user.name }}
            </td>

            <!-- EMAIL -->
            <td class="text-slate-400">
              {{ user.email }}
            </td>

            <!-- ROLE -->
            <td class="text-slate-400">
              {{ user.role }}
            </td>

            <!-- STATUS -->
            <td>
              <span
                class="px-3 py-1 rounded-full text-xs"
                :class="user.status === 'active'
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'"
              >
                {{ user.status }}
              </span>
            </td>

            <!-- ACTIONS -->
            <td class="space-x-2">
              
              <button
                @click.stop="openUser(user)"
                class="px-3 py-1 rounded bg-blue-600/20 text-blue-400 hover:bg-blue-600/40"
              >
                View Details
              </button>
            </td>

          </tr>
        </tbody>

      </table>
      </div>

    </div>

  </div>
</template>