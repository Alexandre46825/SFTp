<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFriendsStore } from '@/stores/friends'
import { useUsersStore } from '@/stores/users'
import { useAuthStore } from '@/stores/Auth'
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()
const friendsStore = useFriendsStore()
const userStore = useUsersStore()
const auth = useAuthStore()

/* =========================
   UI STATE
========================= */
const showAddFriendModal = ref(false)
const searchQuery = ref('')

const selectedFriend = ref(null)
const showModal = ref(false)

/* =========================
   LOAD DATA
========================= */
onMounted(async () => {
  await friendsStore.refreshAll()

  if (userStore.users.length === 0) {
    await userStore.loadUsers()
  }
})

/* =========================
   COMPUTED
========================= */

const friends = computed(() => friendsStore.friends)
const requests = computed(() => friendsStore.requests)

const availableUsers = computed(() => {
  const lowerQuery = searchQuery.value.toLowerCase()
  return userStore.users.filter(user => {
    const isNotFriend = !friendsStore.friends.some(f => f.id_user === user.id_user)
    const isNotSelf = user.id_user !== auth.user.id_user
    const matchesQuery = user.username.toLowerCase().includes(lowerQuery) || user.mail.toLowerCase().includes(lowerQuery)
    return isNotFriend && isNotSelf && matchesQuery
  })
})

/* =========================
   ACTIONS
========================= */
async function addFriend(user) {
  try {
    await friendsStore.addFriend(user.id_user)
    await friendsStore.loadRequests()
    await friendsStore.refreshAll()
    modal.success(
      'Friend Request Sent',
      `A friend request has been sent to ${user.username}.`
    )
  } catch (error) {
    modal.error(
      'Error',
      `An error occurred while trying to send a friend request to ${user.username}.`
    )
  }
}

async function acceptRequest(req) {
  try {
    await friendsStore.acceptFriend(req.id_user)
    await friendsStore.refreshAll()
    modal.success(
      'Friend Request Accepted',
      `You are now friends with ${req.username}.`
    )
  } catch (error) {
    modal.error(
      'Error',
      `An error occurred while trying to accept the friend request from ${req.username}.`
    )
  }
}

async function declineRequest(req) {
  try {
    await friendsStore.removeFriend(req.id_user)
    await friendsStore.refreshAll()
    modal.success(
      'Friend Request Declined',
      `You have declined the friend request from ${req.username}.`
    )
  } catch (error) {
    modal.error(
      'Error',
      `An error occurred while trying to decline the friend request from ${req.username}.`
    )
  }
  await friendsStore.removeFriend(req.id_user)
  await friendsStore.refreshAll()
  modal.success(
    'Friend Request Declined',
    `You have declined the friend request from ${req.username}.`
  )
}

async function removeFriend() {
  if (!selectedFriend.value) return
  try {
    await friendsStore.removeFriend(selectedFriend.value.id_user)
    await friendsStore.refreshAll()
    closeModal()
    modal.success(
      'Friend Removed',
      `You have removed ${selectedFriend.value.username} from your friends.`
    )
  } catch (error) {
    closeModal()
    modal.error(
      'Error',
      `An error occurred while trying to remove ${selectedFriend.value.username}.`
    )
  }

}

/* =========================
   MODALS
========================= */
function openAddFriend() {
  showAddFriendModal.value = true
}

function closeAddFriend() {
  showAddFriendModal.value = false
  searchQuery.value = ''
}

function openProfile(friend) {
  selectedFriend.value = friend
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedFriend.value = null
}
</script>

<template>
  <div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>
      <h1 class="text-3xl font-bold">Network Management</h1>
      <p class="text-slate-400">Manage your connections and relationships</p>
    </div>

    <!-- GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- FRIENDS -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-700 p-4">
        <h2 class="text-xl font-bold mb-4">👥 Amis</h2>

        <div v-if="friends.length === 0" class="text-slate-400 text-sm">
          Aucun ami pour le moment
        </div>

        <div class="space-y-2">
          <div
            v-for="friend in friends"
            :key="friend.id_user"
            @click="openProfile(friend)"
            class="p-3 rounded-xl cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 transition flex justify-between items-center"
          >
            <div>
              <p class="font-semibold">{{ friend.username }}</p>
              <p class="text-sm text-slate-400">{{ friend.mail }}</p>
            </div>

            <span class="text-xs px-2 py-1 rounded-full bg-slate-700 text-slate-200">
              👤
            </span>
          </div>
        </div>
      </div>

      <!-- REQUESTS -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-700 p-4">
        <h2 class="text-xl font-bold mb-4">➕ Demandes</h2>

        <div v-if="requests.length === 0" class="text-slate-400 text-sm">
          Aucune demande
        </div>

        <div class="space-y-3">
          <div
            v-for="req in requests"
            :key="req.id_user"
            class="p-3 bg-slate-900 rounded-xl border border-slate-700"
          >
            <p class="font-semibold">
              {{ req.username || 'Utilisateur inconnu' }}
            </p>
            <p class="text-sm text-slate-400 mb-3">
              {{ req.mail }}
            </p>

            <div class="flex gap-2">
              <button
                @click="acceptRequest(req)"
                class="flex-1 bg-green-600 hover:bg-green-700 py-1 rounded-lg text-sm"
              >
                Accepter
              </button>

              <button
                @click="declineRequest(req)"
                class="flex-1 bg-red-600 hover:bg-red-700 py-1 rounded-lg text-sm"
              >
                Refuser
              </button>
            </div>
          </div>
        </div>

        <button
          @click="openAddFriend"
          class="w-full border border-slate-600 hover:bg-gray-200 dark:hover:bg-gray-700 py-2 rounded-xl mt-4"
        >
          ➕ Ajouter un ami
        </button>
      </div>
    </div>

    <!-- ADD FRIEND MODAL -->
    <div
      v-if="showAddFriendModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click="closeAddFriend"
    >
      <div
        class="bg-white dark:bg-gray-800 w-full max-w-2xl rounded-2xl border border-slate-700 p-6"
        @click.stop
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold">➕ Ajouter un ami</h2>
          <button @click="closeAddFriend">✖</button>
        </div>

        <input
          v-model="searchQuery"
          placeholder="Rechercher..."
          class="w-full p-3 rounded-xl bg-slate-900 border border-slate-700 mb-4"
        />

        <div class="space-y-3 max-h-96 overflow-y-auto">

          <div
            v-for="user in availableUsers"
            :key="user.id_user"
            class="flex justify-between items-center p-4 bg-slate-900 rounded-xl border border-slate-700"
          >
            <div>
              <p class="font-semibold">{{ user.username }}</p>
              <p class="text-sm text-slate-400">{{ user.mail }}</p>
            </div>

            <button
              @click="addFriend(user)"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm"
            >
              Ajouter
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- PROFILE MODAL -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click="closeModal"
    >
      <div
        class="relative bg-white dark:bg-gray-800 w-full max-w-md rounded-2xl border border-slate-700 p-6 shadow-xl"
        @click.stop
      >
        <!-- CLOSE -->
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-slate-400 hover:text-white transition"
        >
          ✖
        </button>

        <div v-if="selectedFriend" class="space-y-6">

          <!-- HEADER -->
          <div class="text-center space-y-1">
            <h2 class="text-2xl font-bold">
              @{{ selectedFriend.username }}
            </h2>

          </div>

          <!-- INFOS -->
          <div class="space-y-3">

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-700">
              <p class="text-xs text-slate-400 mb-1">📧 Email</p>
              <p class="text-sm text-white">
                {{ selectedFriend.mail || 'Not provided' }}
              </p>
            </div>

            <div class="p-3 rounded-xl bg-slate-900 border border-slate-700">
              <p class="text-xs text-slate-400 mb-1">📍 Location</p>
              <p class="text-sm text-white">
                {{ selectedFriend.location || 'Unknown' }}
              </p>
            </div>

          </div>

          <!-- ACTIONS -->
          <div class="space-y-2">

            <!-- REMOVE FRIEND -->
            <button
              @click="removeFriend"
              class="w-full bg-red-600/20 hover:bg-red-600/40 text-red-400 transition py-2 rounded-xl font-semibold border border-red-500/30"
            >
              🗑 Remove friend
            </button>

          </div>

        </div>

      </div>
    </div>

  </div>
</template>