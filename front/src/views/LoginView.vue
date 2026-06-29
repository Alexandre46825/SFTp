<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/Auth'

const router = useRouter()
const authStore = useAuthStore()

const mail = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

async function handleLogin() {

  error.value = null
  loading.value = true

  try {

    await authStore.login({
      mail: mail.value,
      password: password.value
    })

    // redirection après login
    router.push('/')

  } catch (err) {

    error.value =
      err?.response?.data?.detail ||
      'Login failed'

  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-slate-950">

    <div class="w-full max-w-md bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">

      <h1 class="text-3xl font-bold mb-6 text-center">
        Login
      </h1>

      <form
        class="space-y-4"
        @submit.prevent="handleLogin"
      >

        <!-- ERROR -->
        <div
          v-if="error"
          class="bg-red-500/10 text-red-500 p-3 rounded-lg text-sm"
        >
          {{ error }}
        </div>

        <!-- LOGIN -->
        <div>
          <label class="block mb-2">
            Email
          </label>

          <input
            v-model="mail"
            type="text"
            class="w-full p-3 rounded-lg border dark:bg-slate-900"
            required
          >
        </div>

        <!-- PASSWORD -->
        <div>
          <label class="block mb-2">
            Password
          </label>

          <input
            v-model="password"
            type="password"
            class="w-full p-3 rounded-lg border dark:bg-slate-900"
            required
          >
        </div>

        <!-- BUTTON -->
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-3 rounded-lg disabled:opacity-50"
          :disabled="loading"
        >
          <span v-if="!loading">
            Login
          </span>

          <span v-else>
            Logging in...
          </span>
        </button>

        <!-- SIGNUP -->
        <RouterLink
          to="/signup"
          class="block text-center text-blue-500"
        >
          Create an account
        </RouterLink>

      </form>

    </div>
  </div>
</template>