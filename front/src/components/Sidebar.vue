<template>
  <aside class="w-64 bg-slate-800 border-r border-slate-700 p-4">
    <h2 class="text-lg font-bold text-white mb-4">
        User Menu
    </h2>
    <ul class="space-y-2">
        <RouterLink
            to="/"
            class="block rounded-lg px-4 py-3 hover:bg-slate-700"
            >
            🏠 Dashboard
        </RouterLink>
        
        <RouterLink
            to="/network"
            class="block rounded-lg px-4 py-3 hover:bg-slate-700"
            >
           👥 Users and friends
        </RouterLink>
        
        <RouterLink
            to="/upload"
            class="block rounded-lg px-4 py-3 hover:bg-slate-700"
            >
          📤 Send file
        </RouterLink>
    </ul>
    <h2 class="text-lg font-bold text-white mt-8 mb-4">
        Admin Menu
    </h2>
    <ul class="space-y-2">
      <li>
        <a
          href="#"
          class="flex items-center gap-3 p-3 rounded-lg text-slate-300 hover:bg-slate-700 hover:text-white transition"
        >
          ⚙️ Overview
        </a>
      </li>

      <li>
        <a
          href="#"
          class="flex items-center gap-3 p-3 rounded-lg text-slate-300 hover:bg-slate-700 hover:text-white transition"
        >
          📊 Statistics
        </a>
      </li>
        <li>
            <a
            href="#"
            class="flex items-center gap-3 p-3 rounded-lg text-slate-300 hover:bg-slate-700 hover:text-white transition"
            >
            📝 User settings
            </a>
        </li>
    </ul>
  </aside>
</template>