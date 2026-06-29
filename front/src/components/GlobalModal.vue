<script setup>
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()
</script>

<template>
  <Transition name="fade">

    <div
      v-if="modal.show"
      class="fixed inset-0 z-[999] flex items-center justify-center bg-black/60"
    >

      <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-md p-6">

        <div class="flex items-center gap-3 mb-4">

          <div
            class="text-3xl"
            :class="{
              'text-green-500': modal.type === 'success',
              'text-red-500': modal.type === 'error',
              'text-blue-500': modal.type === 'info'
            }"
          >

            <span v-if="modal.type==='success'">✅</span>
            <span v-else-if="modal.type==='error'">❌</span>
            <span v-else>ℹ️</span>

          </div>

          <h2 class="text-xl font-bold text-slate-500 dark:text-slate-300">
            {{ modal.title }}
          </h2>

        </div>

        <p class="text-slate-500 dark:text-slate-300 mb-6">
          {{ modal.message }}
        </p>

        <div class="flex justify-end">

          <button
            @click="modal.close()"
            class="px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
          >
            {{ modal.button }}
          </button>

        </div>

      </div>

    </div>

  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active{
  transition:.2s;
}

.fade-enter-from,
.fade-leave-to{
  opacity:0;
}
</style>