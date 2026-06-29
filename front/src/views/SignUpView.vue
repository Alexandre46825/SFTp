<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/Auth'

const router = useRouter()
const authStore = useAuthStore()

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const email = ref('')

const password = ref('')
const confirmPassword = ref('')

const encryptionPassword = ref('')
const confirmEncryptionPassword = ref('')

const loading = ref(false)
const error = ref(null) 

async function handleRegister() {

  error.value = null

  /* =========================
     VALIDATION FRONT
  ========================= */

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (
    encryptionPassword.value !==
    confirmEncryptionPassword.value
  ) {
    error.value = 'Encryption passwords do not match'
    return
  }

  loading.value = true

  try {

    await authStore.signup({
      name: firstName.value,
      surname: lastName.value,
      username: username.value,
      mail: email.value,
      password: password.value,
      password_pgp: encryptionPassword.value,
      location: "Unknown"
    })

    // redirection vers login après inscription
    router.push('/login')

  } catch (err) {

    error.value =
      err?.response?.data?.detail ||
      'Signup failed'

  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-slate-950 p-4">

    <div class="w-full max-w-2xl bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">

      <h1 class="text-3xl font-bold mb-6 text-center">
        Create account
      </h1>

      <form
        class="grid md:grid-cols-2 gap-4"
        @submit.prevent="handleRegister"
      >

        <!-- ERROR -->
        <div
          v-if="error"
          class="md:col-span-2 bg-red-500/10 text-red-500 p-3 rounded-lg text-sm"
        >
          {{ error }}
        </div>

        <!-- FIRST NAME -->
        <div>
          <label>First name</label>
          <input
            v-model="firstName"
            type="text"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- LAST NAME -->
        <div>
          <label>Last name</label>
          <input
            v-model="lastName"
            type="text"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- USERNAME -->
        <div>
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- EMAIL -->
        <div>
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- PASSWORD -->
        <div>
          <label>Password</label>
          <input
            v-model="password"
            type="password"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- CONFIRM PASSWORD -->
        <div>
          <label>Confirm password</label>
          <input
            v-model="confirmPassword"
            type="password"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- ENCRYPTION PASSWORD -->
        <div>
          <label>Encryption password</label>
          <input
            v-model="encryptionPassword"
            type="password"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- CONFIRM ENCRYPTION -->
        <div>
          <label>Confirm encryption password</label>
          <input
            v-model="confirmEncryptionPassword"
            type="password"
            class="w-full p-3 rounded-lg border bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
        </div>

        <!-- SUBMIT -->
        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full bg-blue-600 text-slate-900 dark:text-white py-3 rounded-lg disabled:opacity-50"
            :disabled="loading"
          >
            <span v-if="!loading">
              Create account
            </span>

            <span v-else>
              Creating account...
            </span>
          </button>
        </div>

      </form>

      <RouterLink
        to="/login"
        class="block mt-4 text-center text-blue-500"
      >
        Already have an account?
      </RouterLink>

    </div>

  </div>
</template>