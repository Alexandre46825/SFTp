<script setup>
defineProps({
  title: String,
  value: String,
})
</script>

<template>
  <div class="bg-slate-800 rounded-xl p-6 border border-slate-700">
    <p class="text-slate-400 text-sm">
      {{ title }}
    </p>

    <h3 class="text-3xl font-bold mt-2">
      {{ value }}
    </h3>
  </div>
</template>