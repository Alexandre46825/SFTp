<script setup>
defineProps({
  title: String,
  value: String,
})
</script>

<template>
  <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
    <p class="text-slate-400 text-sm">{{ title }}</p>
    <p class="text-2xl font-bold">{{ value }}</p>
  </div>
</template>

