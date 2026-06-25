<script setup>
import { useAuthStore } from '@/stores/Auth'

const auth = useAuthStore()

auth.fetchUser()
</script>

<template>
  <RouterView />
</template>