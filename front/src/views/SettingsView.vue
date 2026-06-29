<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/Auth'
import { useRouter } from 'vue-router'
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()
const auth = useAuthStore()
const router = useRouter()

// -------------------
// PROFILE FIELDS
// -------------------
const username = ref(auth.user?.username || '')
const location = ref(auth.user?.location || '')

// -------------------
// PASSWORD FIELDS
// -------------------
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

// -------------------
// SAVE PROFILE
// -------------------
async function saveProfile() {
  try {
    await auth.updateProfile({
      username: username.value,
      location: location.value
    })

    modal.success('Profile Updated', 'Your profile has been successfully updated.')
  } catch (e) {
    modal.error('Error', 'An error occurred while updating the profile.')
  }
}

// -------------------
// CHANGE PASSWORD
// -------------------
async function changePassword() {
  if (newPassword.value !== confirmPassword.value) {
    modal.error('Error', 'The passwords do not match.')
    return
  }

  try {
    const res = await auth.changePassword({
      old_password: oldPassword.value,
      new_password: newPassword.value
    })
    console.log(res)
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''

    modal.success('Password Updated', 'Your password has been successfully updated.')
  } catch (e) {
    modal.error('Error', 'An error occurred while updating the password.')
  }
}

// -------------------
// LOGOUT
// -------------------
function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="p-6 space-y-8">

    <h2 class="text-3xl font-bold">
      Settings
    </h2>

    <!-- PROFILE -->
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 space-y-5">

      <h3 class="text-xl font-semibold">
        Profile
      </h3>

      <!-- Username -->
      <div class="space-y-2">
        <label class="text-sm text-slate-400">
          Username
        </label>
        <input
          v-model="username"
          type="text"
          class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-blue-500 outline-none"
        >
      </div>

      <!-- Location -->
      <div class="space-y-2">
        <label class="text-sm text-slate-400">
          Location
        </label>
        <input
          v-model="location"
          type="text"
          class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-blue-500 outline-none"
        >
      </div>

      <button
        class="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg"
        @click="saveProfile"
      >
        Save changes
      </button>

    </div>

    <!-- PASSWORD -->
    <div class="bg-white dark:bg-gray-800 p-6 rounded-xl border border-slate-200 dark:border-slate-700 space-y-5">

      <h3 class="text-xl font-semibold">
        Change password
      </h3>

      <!-- Old password -->
      <div class="space-y-2">
        <label class="text-sm text-slate-400">
          Current password
        </label>
        <input
          v-model="oldPassword"
          type="password"
          class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-yellow-500 outline-none"
        >
      </div>

      <!-- New password -->
      <div class="space-y-2">
        <label class="text-sm text-slate-400">
          New password
        </label>
        <input
          v-model="newPassword"
          type="password"
          class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-yellow-500 outline-none"
        >
      </div>

      <!-- Confirm password -->
      <div class="space-y-2">
        <label class="text-sm text-slate-400">
          Confirm password
        </label>
        <input
          v-model="confirmPassword"
          type="password"
          class="w-full rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 border border-slate-200 dark:border-slate-700 p-3 focus:border-yellow-500 outline-none"
        >
      </div>

      <button
        class="w-full bg-yellow-600 hover:bg-yellow-700 py-3 rounded-lg"
        @click="changePassword"
      >
        Update password
      </button>

    </div>

    <!-- LOGOUT -->
    <div class="p-6 rounded-xl">


      <button
        class="w-full bg-red-600 hover:bg-red-700 py-3 rounded-lg"
        @click="logout"
      >
        Sign out
      </button>

    </div>

  </div>
</template>