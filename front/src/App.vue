<script setup>
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="h-screen flex flex-col bg-slate-900 text-white">
    <Navbar />

    <div class="flex flex-1 overflow-hidden">
      <Sidebar />

      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>