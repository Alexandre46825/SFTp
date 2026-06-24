<script setup>
import { ref, computed } from 'vue'

/* =========================
   MOCK USER (sera API plus tard)
========================= */

const user = ref({
  id: 1,
  firstName: 'Marc',
  lastName: 'Dupont',
  email: 'marc@mail.com',
  location: 'France, Paris',
  role: 'user',
  status: 'active',
  lastLogin: '2 hours ago',

  friends: [
    '@lea',
    '@alex',
    '@julie'
  ],

  logs: [
    { id: 1, text: 'Logged in', time: '2h ago' },
    { id: 2, text: 'Uploaded project.zip', time: '3h ago' },
    { id: 3, text: 'Added @lea as friend', time: '1d ago' }
  ],

  files: [
    { id: 1, name: 'project.zip', size: '84MB', date: 'Today' },
    { id: 2, name: 'design.fig', size: '12MB', date: 'Yesterday' },
    { id: 3, name: 'notes.txt', size: '2MB', date: '3 days ago' }
  ]
})

/* =========================
   ACTIONS (mock frontend)
========================= */

function toggleBan() {
  user.value.status =
    user.value.status === 'banned' ? 'active' : 'banned'
}

function deleteUser() {
  alert('User deleted (mock)')
}
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">
          {{ user.firstName }} {{ user.lastName }}
        </h1>
        <p class="text-slate-400">{{ user.email }}</p>
      </div>

      <div class="space-x-2">
        <button
          @click="toggleBan"
          class="px-4 py-2 rounded bg-yellow-600/20 text-yellow-400"
        >
          {{ user.status === 'banned' ? 'Unban' : 'Ban' }}
        </button>

        <button
          @click="deleteUser"
          class="px-4 py-2 rounded bg-red-600/20 text-red-400"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- INFO GRID -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <p class="text-slate-400 text-sm">Location</p>
        <p class="font-semibold">{{ user.location }}</p>
      </div>

      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <p class="text-slate-400 text-sm">Last login</p>
        <p class="font-semibold">{{ user.lastLogin }}</p>
      </div>

      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <p class="text-slate-400 text-sm">Status</p>

        <span
          class="px-3 py-1 rounded-full text-xs"
          :class="user.status === 'active'
            ? 'bg-green-500/20 text-green-400'
            : 'bg-red-500/20 text-red-400'"
        >
          {{ user.status }}
        </span>
      </div>
    
    <!-- ROLE -->

      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <p class="text-slate-400 text-sm mb-2">Role</p>

        <select
          v-model="user.role"
          class="bg-slate-800 border border-slate-700 p-2 rounded"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>

    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">

      <!-- FRIENDS -->
      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <h2 class="text-lg font-semibold mb-3">Friends</h2>

        <div class="space-y-2">
          <div
            v-for="f in user.friends"
            :key="f"
            class="bg-slate-800 p-2 rounded"
          >
            {{ f }}
          </div>
        </div>
      </div>

      <!-- LOGS -->
      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <h2 class="text-lg font-semibold mb-3">Activity logs</h2>

        <div class="space-y-2 text-sm">
          <div
            v-for="log in user.logs"
            :key="log.id"
            class="bg-slate-800 p-2 rounded flex justify-between"
          >
            <span>{{ log.text }}</span>
            <span class="text-slate-400">{{ log.time }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- FILES -->
    <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
      <h2 class="text-lg font-semibold mb-3">Recent files</h2>

      <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[700px]">
          <thead class="text-slate-400 text-left">
            <tr>
              <th>File</th>
              <th>Size</th>
              <th>Date</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="file in user.files"
            :key="file.id"
            class="border-t border-slate-800"
          >
            <td class="py-2">{{ file.name }}</td>
            <td class="text-slate-400">{{ file.size }}</td>
            <td class="text-slate-400">{{ file.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>

  </div>
</template>