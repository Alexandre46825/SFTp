<script setup>
import { ref, computed, onMounted } from 'vue'
import StatCard from '../components/StatCard.vue'

/* =========================
   MOCK DATA (plus tard API)
========================= */

const stats = ref({
  users: 128,
  activeUsers: 34,
  files: 842,
  storageUsed: 2.4, // GB
  storageMax: 10,   // GB
  uploadsToday: 27,
  shares: 56
})

const activities = ref([
  { id: 1, text: 'Marc uploaded project.zip', type: 'upload' },
  { id: 2, text: 'Léa added @Thomas', type: 'friend' },
  { id: 3, text: 'File shared with @Alex', type: 'share' },
  { id: 4, text: 'Upload failed: large_video.mp4', type: 'error' }
])

const users = ref([
  { id: 1, name: 'Marc', email: 'marc@mail.com', lastLogin: '2h ago' },
  { id: 2, name: 'Léa', email: 'lea@mail.com', lastLogin: '1d ago' },
  { id: 3, name: 'Alex', email: 'alex@mail.com', lastLogin: '5m ago' }
])

const files = ref([
  { id: 1, name: 'project.zip', owner: 'Marc', size: '84MB', date: 'Today' },
  { id: 2, name: 'design.fig', owner: 'Léa', size: '12MB', date: 'Yesterday' },
  { id: 3, name: 'video.mp4', owner: 'Alex', size: '240MB', date: '2 days ago' }
])

/* =========================
   COMPUTED
========================= */

const storagePercent = computed(() =>
  (stats.value.storageUsed / stats.value.storageMax) * 100
)
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">Admin Overview</h1>
      <p class="text-slate-400">System activity & statistics</p>
    </div>

    <!-- KPI CARDS -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

      <StatCard title="Total Users" :value="stats.users.toString()" />
      <StatCard title="Active Users" :value="stats.activeUsers.toString()" />
      <StatCard title="Files Sent" :value="stats.files.toString()" />
      <StatCard title="Uploads Today" :value="stats.uploadsToday.toString()" />

    </div>

    <!-- STORAGE -->
    <div class="bg-slate-900 p-6 rounded-xl border border-slate-700">
      <div class="flex justify-between mb-2">
        <p class="font-medium">Storage usage</p>
        <p class="text-slate-400 text-sm">
          {{ stats.storageUsed }}GB / {{ stats.storageMax }}GB
        </p>
      </div>

      <div class="w-full bg-slate-700 rounded-full h-3">
        <div
          class="h-3 bg-blue-500 rounded-full"
          :style="{ width: storagePercent + '%' }"
        />
      </div>
    </div>

    <!-- MAIN GRID -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">

      <!-- ACTIVITY -->
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-700">
        <h2 class="text-xl font-semibold mb-4">Recent activity</h2>

        <div class="space-y-3">
          <div
            v-for="a in activities"
            :key="a.id"
            class="p-3 bg-slate-800 rounded-lg"
          >
            <p class="text-sm">{{ a.text }}</p>
          </div>
        </div>
      </div>

      <!-- USERS -->
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-700">
        <h2 class="text-xl font-semibold mb-4">Users</h2>
        <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[700px]">
          <thead class="text-slate-400 text-left">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Last login</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="u in users"
              :key="u.id"
              class="border-t border-slate-800"
            >
              <td class="py-2">{{ u.name }}</td>
              <td class="py-2 text-slate-400">{{ u.email }}</td>
              <td class="py-2 text-slate-400">{{ u.lastLogin }}</td>
            </tr>
          </tbody>
        </table>
        </div>
      </div>

    </div>

    <!-- FILES -->
    <div class="bg-slate-900 p-6 rounded-xl border border-slate-700">
      <h2 class="text-xl font-semibold mb-4">Recent files</h2>

      <div class="overflow-x-auto">
        <table class="w-full text-sm min-w-[700px]">
          <thead class="text-slate-400 text-left">
            <tr>
              <th>File</th>
              <th>Owner</th>
              <th>Size</th>
            <th>Date</th>
          </tr>
            </thead>

            <tbody>
            <tr
                v-for="f in files"
                :key="f.id"
                class="border-t border-slate-800"
            >
                <td class="py-2">{{ f.name }}</td>
                <td class="py-2 text-slate-400">{{ f.owner }}</td>
                <td class="py-2 text-slate-400">{{ f.size }}</td>
                <td class="py-2 text-slate-400">{{ f.date }}</td>
            </tr>
            </tbody>
        </table>
      </div>
    </div>

  </div>
</template>