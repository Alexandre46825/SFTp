<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminUsersStore } from '@/stores/adminUsers'

const router = useRouter()
const adminUsers = useAdminUsersStore()

const search = ref('')
const sortKey = ref('name')
const sortOrder = ref('asc')

onMounted(() => {
  adminUsers.fetchUsers()
})

function sortBy(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const filteredUsers = computed(() => {
  let users = adminUsers.users || []

  // SEARCH
  users = users.filter(u =>
    (u.name || '').toLowerCase().includes(search.value.toLowerCase()) ||
    (u.mail || '').toLowerCase().includes(search.value.toLowerCase()) ||
    (u.is_admin ? 'admin' : 'user').includes(search.value.toLowerCase())
  )

  // SORT
  users.sort((a, b) => {
    const aVal = getValue(a, sortKey.value)
    const bVal = getValue(b, sortKey.value)

    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })

  return users
})

function getValue(user, key) {
  switch (key) {
    case 'name': return user.name?.toLowerCase() || ''
    case 'mail': return user.mail?.toLowerCase() || ''
    case 'role': return user.is_admin ? 'admin' : 'user'
    case 'status': return user.account_status ?? 0
    default: return ''
  }
}

function openUser(user) {
  router.push(`/admin/users/${user.id_user}`)
}

</script>

<template>
  <div class="p-6 space-y-8">

    <h1 class="text-3xl font-bold">Users management</h1>

    <input
      v-model="search"
      placeholder="Search user..."
      class="w-full md:w-1/3 p-3 rounded-xl bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700"
    />

<div class="bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">      <table class="w-full text-sm">
        <thead class="bg-slate-800 text-slate-400 text-left">
          <tr>
            <th class="p-3 cursor-pointer" @click="sortBy('name')">
              Name | Surname
              <span v-if="sortKey === 'name'">▲▼</span>
            </th>


            <th class="p-3 cursor-pointer" @click="sortBy('username')">
              Username
              <span v-if="sortKey === 'username'">▲▼</span>
            </th>

            <th class="cursor-pointer" @click="sortBy('mail')">
              Email
              <span v-if="sortKey === 'mail'">▲▼</span>
            </th>

            <th class="cursor-pointer" @click="sortBy('role')">
              Role
              <span v-if="sortKey === 'role'">▲▼</span>
            </th>

            <th class="cursor-pointer" @click="sortBy('status')">
              Status
              <span v-if="sortKey === 'status'">▲▼</span>
            </th>

            <th>Consult</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="user in filteredUsers"
            :key="user.id"
            class="border-t border-slate-800 hover:bg-slate-800/40"
          >

            <td class="p-3 cursor-pointer" @click="openUser(user)">
              {{ user.name }} | {{ user.surname }}
            </td>

            <td class="p-3 cursor-pointer" @click="openUser(user)">
              {{ user.username }}
            </td>

            <td class="text-slate-400">
              {{ user.mail }}
            </td>

            <td class="text-slate-400">
              {{ user.is_admin ? 'Admin' : 'User' }}
            </td>

            <td>
              <span
                class="px-2 py-1 rounded text-xs"
                :class="user.account_status == 1
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'"
              >
                {{ user.account_status == 2 ? 'Banned' : (user.account_status == 1 ? 'Active' : 'Deleted') }}
              </span>
            </td>

            <td class="space-x-2">

              <button
                @click="openUser(user)"
                class="px-3 py-1 rounded bg-blue-600/20 text-blue-400"
              >
                View
              </button>

            </td>

          </tr>
        </tbody>

      </table>
    </div>
    <div class="text-sm text-slate-400">
      {{ filteredUsers.length }} users found
    </div>

  </div>
</template>