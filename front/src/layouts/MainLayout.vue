<script setup>
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
</script>

<template>
	<div class="h-screen flex flex-col bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 text-black dark:text-slate-900 dark:text-white">
		<Navbar />

		<div class="flex flex-1 overflow-hidden">
		<Sidebar />

		<main class="flex-1 overflow-y-auto p-6 bg-white dark:bg-gray-800">
			<router-view />
		</main>
		</div>
	</div>
</template>