<script setup>
import { onMounted } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
)

/* =========================
   MOCK DATA (backend later)
========================= */

const fileTransfersData = {
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  data: [12, 19, 8, 15, 22, 30, 18]
}

const loginData = {
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  data: [50, 80, 65, 90, 120, 140, 110]
}

/* =========================
   CHART INIT
========================= */

onMounted(() => {
  const ctx1 = document.getElementById('filesChart')
  const ctx2 = document.getElementById('loginChart')

  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: fileTransfersData.labels,
      datasets: [{
        label: 'File transfers',
        data: fileTransfersData.data,
        borderColor: '#3b82f6',
        tension: 0.3
      }]
    }
  })

  new Chart(ctx2, {
    type: 'line',
    data: {
      labels: loginData.labels,
      datasets: [{
        label: 'User logins',
        data: loginData.data,
        borderColor: '#22c55e',
        tension: 0.3
      }]
    }
  })
})
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">Statistics</h1>
      <p class="text-slate-400">Global activity overview</p>
    </div>


    <!-- GRAPHS -->
    <div class="grid grid-cols-1 lg:grid-cols-1 md:grid-cols-1 gap-6">

      <!-- FILE TRANSFERS -->
      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <h2 class="text-lg font-semibold mb-4">
          File transfers
        </h2>

        <canvas id="filesChart"></canvas>
      </div>

      <!-- LOGINS -->
      <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
        <h2 class="text-lg font-semibold mb-4">
          User logins
        </h2>

        <canvas id="loginChart"></canvas>
      </div>

    </div>


  </div>
</template>