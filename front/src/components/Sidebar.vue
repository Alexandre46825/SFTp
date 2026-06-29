<script setup>
import { useSidebarStore } from '@/stores/sidebar'
import { useAuthStore } from '@/stores/Auth'

const sidebar = useSidebarStore()
const auth = useAuthStore()
</script>

<template>
  <aside
    v-show="sidebar.isOpen"
    class="w-64 bg-white dark:bg-gray-800 border-r border-slate-700 p-4"
  >
    <h2 class="text-lg font-bold text-black dark:text-white mb-4">
        User Menu
    </h2>
    <ul class="space-y-2">
        <RouterLink
            to="/"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
            🏠 Dashboard
        </RouterLink>
        
        <RouterLink
            to="/network"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
           👥 Users and friends
        </RouterLink>
        
        <RouterLink
            to="/upload"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
          📤 Send file
        </RouterLink>
    </ul>
    <div v-if="auth.isAdmin">
    <h2 class="text-lg font-bold text-black dark:text-white mt-8 mb-4">
        Admin Menu
    </h2>
    <ul class="space-y-2">
        <RouterLink
            to="/admin"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
          ⚙️ Overview
        </RouterLink>

        
        <RouterLink
            to="/admin/users"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
          📝 User settings
        </RouterLink>
        <RouterLink
            to="/admin/logs"
            class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-slite-800 hover:text-black dark:text-white transition"
            >
          📜 Logs
        </RouterLink>
    </ul>
    </div>
  </aside>
</template>