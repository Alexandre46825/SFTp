<script setup>
import StatCard from '../components/StatCard.vue'
</script>

<template>
  <div class="space-y-6">
    <h2 class="text-3xl font-bold">
      Tableau de bord
    </h2>

    <div class="grid gap-6 md:grid-cols-3">
      <StatCard title="Fichiers envoyés" value="128" />
      <StatCard title="Utilisateurs actifs" value="34" />
      <StatCard title="Stockage utilisé" value="18 Go" />
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h3 class="text-xl font-semibold mb-4">
          Activité récente
        </h3>

        <p class="text-slate-400">
          Liste des dernières actions réalisées.
        </p>
      </div>

      <div class="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h3 class="text-xl font-semibold mb-4">
          Notifications
        </h3>

        <p class="text-slate-400">
          Aucun événement important.
        </p>
      </div>
    </div>
  </div>
</template>