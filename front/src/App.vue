<script setup>
import { useAuthStore } from '@/stores/Auth'
import GlobalModal from '@/components/GlobalModal.vue'
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()

const auth = useAuthStore()

auth.fetchUser()
</script>

<template>
  <RouterView />
  <GlobalModal />
</template>