<script setup>
import { ref, computed, onMounted } from 'vue'
import StatCard from '@/components/StatCard.vue'
import api from '@/services/api'

const overview = ref({
  total_users: 0,
  files_sent: 0,
  uploads_today: 0,
  storage_used_gb: 0,
  storage_used_bytes: 0
})

const loading = ref(true)

async function loadOverview() {
  loading.value = true

  try {
    const { data } = await api.get('/admin/overview')
    overview.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadOverview)

/* =========================
   COMPUTED
========================= */

const storageUsed = computed(() =>
  Number(overview.value.storage_used_gb).toFixed(2)
)

// Si tu connais la capacité max de ton serveur,
// modifie simplement cette valeur.
const storageMax = 10

const storagePercent = computed(() => {
  return Math.min(
    (overview.value.storage_used_gb / storageMax) * 100,
    100
  )
})
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">
        Admin Overview
      </h1>

      <p class="text-slate-400">
        System activity & statistics
      </p>
    </div>

    <!-- LOADING -->
    <div
      v-if="loading"
      class="text-center text-slate-400 py-20"
    >
      Loading overview...
    </div>

    <template v-else>

      <!-- KPI -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

        <StatCard
          title="Total Users"
          :value="overview.total_users.toString()"
        />

        <StatCard
          title="Files Sent"
          :value="overview.files_sent.toString()"
        />

        <StatCard
          title="Uploads Today"
          :value="overview.uploads_today.toString()"
        />


      </div>

      <!-- STORAGE -->
      <div class="bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-2xl p-6">

        <div class="flex justify-between items-center mb-4">

          <div>
            <h2 class="text-xl font-semibold">
              Storage Usage
            </h2>

            <p class="text-sm text-slate-400">
              {{ overview.storage_used_bytes.toLocaleString() }} bytes
            </p>
          </div>

          <div class="text-right">
            <p class="font-semibold">
              {{ storageUsed }} GB / {{ storageMax }} GB
            </p>
          </div>

        </div>

        <div class="w-full h-3 bg-slate-700 rounded-full overflow-hidden">

          <div
            class="h-full bg-blue-500 transition-all duration-500"
            :style="{ width: storagePercent + '%' }"
          />

        </div>

        <p class="text-right text-sm text-slate-400 mt-2">
          {{ storagePercent.toFixed(1) }}%
        </p>

      </div>

    </template>

  </div>
</template>