<script setup>
import { ref, computed } from 'vue'

const showAddFriendModal = ref(false)
const searchQuery = ref('')
const filterStatus = ref('all')


function openAddFriend() {
  showAddFriendModal.value = true
}

function closeAddFriend() {
  showAddFriendModal.value = false
  searchQuery.value = ''
  filterStatus.value = 'all'
}

function sendRequest(user) {
  user.relation = 'pending'
}

// filtre dynamique
const filteredUsers = computed(() => {
  return users.value
    .filter(u => u.relation === 'none')
    .filter(user => {
      const matchSearch =
        user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        user.username.toLowerCase().includes(searchQuery.value.toLowerCase())

      const matchFilter =
        filterStatus.value === 'all' ||
        user.status === filterStatus.value

      return matchSearch && matchFilter
    })
})
const users = ref([
  {
    id: 101,
    name: 'Emma Laurent',
    username: '@emma',
    location: 'Laval',
    mail: 'test@example.com',
    status: 'En ligne',
    role: 'Frontend Dev',
    relation: 'none',
  },
  {
    id: 102,
    name: 'Lucas Morel',
    username: '@lucas',
    location: 'Lyon',
    mail: 'lucas@example.com',
    status: 'Hors ligne',
    role: 'Backend Dev',
    relation: 'friend',
  },
  {
    id: 103,
    name: 'Sarah Lopez',
    username: '@sarah',
    location: 'Marseille',
    mail: 'sarah@example.com',
    status: 'Absent',
    role: 'UI Designer',
    relation: 'received',
  },
])

const friends = computed(() =>
  users.value.filter(u => u.relation === 'friend')
)

const requests = computed(() =>
  users.value.filter(u => u.relation === 'received')
)

const suggestions = computed(() =>
  users.value.filter(u => u.relation === 'none')
)

const selectedFriend = ref(null)
const showModal = ref(false)

function openProfile(friend) {
  selectedFriend.value = friend
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedFriend.value = null
}

function acceptRequest(id) {
  const user = users.value.find(u => u.id === id)
  if (!user) return

  user.relation = 'friend'
}

function declineRequest(id) {
  const user = users.value.find(u => u.id === id)
  if (!user) return

  user.relation = 'none'
}
</script>

<template>
  <div class="p-6 space-y-8">

    <div>
      <h1 class="text-3xl font-bold">Network Management</h1>
      <p class="text-slate-400">Manage your connections and relationships</p>
    </div>

  <div class="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-1 gap-4">

    <!-- LISTE AMIS -->
    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-700 p-4">
      <h2 class="text-xl font-bold mb-4">👥 Amis</h2>

      <div class="space-y-2">
        <div
          v-for="friend in friends"
          :key="friend.id"
          @click="openProfile(friend)"
          class="p-3 rounded-xl cursor-pointer hover:bg-gray-200 dark:hover:bg-slite-800 transition flex justify-between items-center"
        >
          <div>
            <p class="font-semibold">{{ friend.name }}</p>
            <p class="text-sm text-slate-400">{{ friend.username }}</p>
          </div>

          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="{
              'bg-green-500/20 text-green-400': friend.status === 'En ligne',
              'bg-yellow-500/20 text-yellow-400': friend.status === 'Absent',
              'bg-slate-600 text-slate-300': friend.status === 'Hors ligne',
            }"
          >
            {{ friend.status }}
          </span>
        </div>
      </div>
    </div>

    <!-- DEMANDES -->
    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-slate-700 p-4">
      <h2 class="text-xl font-bold mb-4">➕ Demandes d'amis</h2>

      <div class="space-y-3">
        <div
          v-for="req in requests"
          :key="req.id"
          class="p-3 bg-slate-900 rounded-xl border border-slate-700"
        >
          <p class="font-semibold">{{ req.name }}</p>
          <p class="text-sm text-slate-400 mb-3">{{ req.username }}</p>

          <div class="flex gap-2">
            <button
              @click="acceptRequest(req.id)"
              class="flex-1 bg-green-600 hover:bg-green-700 py-1 rounded-lg text-sm"
            >
              Accepter
            </button>

            <button
              @click="declineRequest(req.id)"
              class="flex-1 bg-red-600 hover:bg-red-700 py-1 rounded-lg text-sm"
            >
              Refuser
            </button>
          </div>
        </div>

        <button
        @click="openAddFriend"
        class="w-full border border-slate-600 hover:bg-gray-200 dark:hover:bg-slite-800 py-2 rounded-xl mt-4"
        >
        ➕ Ajouter un ami
        </button>
      </div>
    </div>
<!-- MODALE AJOUT AMI -->
<div
  v-if="showAddFriendModal"
  class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
  @click="closeAddFriend"
>
  <div
    class="bg-white dark:bg-gray-800 w-full max-w-2xl rounded-2xl border border-slate-700 p-6"
    @click.stop
  >
    <!-- HEADER -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold">
        ➕ Ajouter un ami
      </h2>

      <button
        @click="closeAddFriend"
        class="text-slate-400 hover:text-black dark:text-white"
      >
        ✖
      </button>
    </div>

    <!-- SEARCH + FILTER -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Rechercher un utilisateur..."
        class="w-full p-3 rounded-xl bg-slate-900 border border-slate-700"
      />

      <select
        v-model="filterStatus"
        class="w-full p-3 rounded-xl bg-slate-900 border border-slate-700"
      >
        <option value="all">Tous les statuts</option>
        <option value="En ligne">En ligne</option>
        <option value="Absent">Absent</option>
        <option value="Hors ligne">Hors ligne</option>
      </select>
    </div>

    <!-- LISTE UTILISATEURS -->
    <div class="space-y-3 max-h-96 overflow-y-auto pr-2">
      <div
        v-for="user in filteredUsers"
        :key="user.id"
        class="flex items-center justify-between p-4 bg-slate-900 border border-slate-700 rounded-xl"
      >
        <div>
          <p class="font-semibold">
            {{ user.name }}
          </p>

          <p class="text-sm text-slate-400">
            {{ user.username }} · {{ user.role }}
          </p>

          <p class="text-xs text-slate-500 mt-1">
            {{ user.status }}
          </p>
        </div>

        <button
            @click="sendRequest(user)"
            class="px-4 py-2 rounded-lg text-sm"
            :class="{
                'bg-blue-600 hover:bg-blue-700': user.relation === 'none',
                'bg-yellow-600 cursor-not-allowed': user.relation === 'pending',
            }"
            :disabled="user.relation !== 'none'"
            >
            {{ user.relation === 'pending' ? 'Demande envoyée' : 'Ajouter' }}
        </button>
      </div>

      <p
        v-if="filteredUsers.length === 0"
        class="text-slate-400 text-center py-6"
      >
        Aucun utilisateur trouvé
      </p>
    </div>
  </div>
</div>


    <!-- MODALE PROFIL -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click="closeModal"
    >
      <div
        class="bg-white dark:bg-gray-800 w-full max-w-md rounded-2xl border border-slate-700 p-6 relative"
        @click.stop
      >
        <!-- bouton fermer -->
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-slate-400 hover:text-black dark:text-white"
        >
          ✖
        </button>

        <div v-if="selectedFriend" class="space-y-4">
          <div>
            <h2 class="text-2xl font-bold">
              {{ selectedFriend.name }}
            </h2>
            <p class="text-slate-400">
              {{ selectedFriend.username }}
            </p>
          </div>

          <div class="space-y-1 text-sm text-slate-300">
            <p>📍 {{ selectedFriend.location }}</p>
            <p>💼 {{ selectedFriend.role }}</p>
            <p>🟢 {{ selectedFriend.status }}</p>
          </div>

          <div class="bg-slate-900 p-4 rounded-xl border border-slate-700">
            <p class="text-slate-300">
              {{ selectedFriend.bio }}
            </p>
          </div>

          <button class="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-xl font-semibold">
            💬 Envoyer un message
          </button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>