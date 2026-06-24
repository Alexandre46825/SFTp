<script setup>
import { ref } from 'vue'

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const email = ref('')

const password = ref('')
const confirmPassword = ref('')

const encryptionPassword = ref('')
const confirmEncryptionPassword = ref('')

function handleRegister() {

  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }

  if (
    encryptionPassword.value !==
    confirmEncryptionPassword.value
  ) {
    alert('Encryption passwords do not match')
    return
  }

  console.log({
    firstName: firstName.value,
    lastName: lastName.value,
    username: username.value,
    email: email.value,
    password: password.value,
    encryptionPassword: encryptionPassword.value
  })
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen p-4">

    <div class="w-full max-w-2xl bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">

      <h1 class="text-3xl font-bold mb-6 text-center">
        Create account
      </h1>

      <form
        class="grid md:grid-cols-2 gap-4"
        @submit.prevent="handleRegister"
      >

        <div>
          <label>First name</label>
          <input
            v-model="firstName"
            type="text"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Last name</label>
          <input
            v-model="lastName"
            type="text"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Password</label>
          <input
            v-model="password"
            type="password"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Confirm password</label>
          <input
            v-model="confirmPassword"
            type="password"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Encryption password</label>
          <input
            v-model="encryptionPassword"
            type="password"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div>
          <label>Confirm encryption password</label>
          <input
            v-model="confirmEncryptionPassword"
            type="password"
            class="w-full p-3 rounded-lg border"
            required
          >
        </div>

        <div class="md:col-span-2">
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-3 rounded-lg"
          >
            Create account
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