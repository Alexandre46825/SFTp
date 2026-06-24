<script setup>
import StatCard from '@/components/StatCard.vue'
</script>

<template>
  <div class="p-6 space-y-8">
    
    <div>
      <h1 class="text-3xl font-bold">User Dashboard</h1>
      <p class="text-slate-400">Welcome back! Here's what's happening with your account.</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <StatCard title="Fichiers envoyés" value="128" />
      <StatCard title="Utilisateurs actifs" value="34" />
      <StatCard title="Stockage utilisé" value="18 Go" />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
      <StatCard title="Activité récente" value="Liste des dernières actions réalisées." />
      <StatCard title="Notifications" value="Aucun événement important." />
    </div>
  </div>
</template>