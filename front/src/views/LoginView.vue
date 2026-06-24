.<script setup>
import { ref } from 'vue'

const login = ref('')
const password = ref('')

function handleLogin() {
  console.log({
    login: login.value,
    password: password.value
  })
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">

      <h1 class="text-3xl font-bold mb-6 text-center">
        Login
      </h1>

      <form
        class="space-y-4"
        @submit.prevent="handleLogin"
      >

        <div>
          <label class="block mb-2">
            Email or Username
          </label>

          <input
            v-model="login"
            type="text"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label class="block mb-2">
            Password
          </label>

          <input
            v-model="password"
            type="password"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-3 rounded-lg"
        >
          Login
        </button>

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