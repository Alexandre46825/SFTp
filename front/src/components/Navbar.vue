<script setup>
import { useSidebarStore } from '@/stores/sidebar'

const sidebar = useSidebarStore()

</script>

<template>
  <header class="h-16 bg-white dark:bg-gray-800 border-b border-slate-700 px-6 flex items-center justify-between">

    <!-- LEFT -->
     
    <div class="flex items-center gap-6">
    <button
    @click="sidebar.toggleSidebar()"
    class="text-slate-300 hover:text-blue-400 transition"
    >
    ☰
    </button>
    <h1 class="text-xl font-bold text-black dark:text-white flex items-center gap-2">
      <img src="/img/logo.png" class="h-8" />
      SFTP
    </h1>
    </div>

    <!-- RIGHT -->
    <div class="flex items-center gap-6">


      <nav>
        <ul class="flex gap-6 text-slate-300">

          <RouterLink to="/settings" class="hover:text-blue-400">
            Account
          </RouterLink>
        </ul>
      </nav>

    </div>

  </header>
</template>