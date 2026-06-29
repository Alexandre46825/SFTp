<script setup>
defineProps({
  title: String,
  value: String,
})
</script>

<template>
  <div class="bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
    <p class="text-slate-400 text-sm">{{ title }}</p>
    <p class="text-2xl font-bold">{{ value }}</p>
  </div>
</template>

