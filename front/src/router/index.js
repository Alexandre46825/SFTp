import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/Auth'

import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import HomeView from '../views/HomeView.vue'

import FilesView from '../views/FilesView.vue'
import UploadView from '../views/UploadView.vue'
import SettingsView from '../views/SettingsView.vue'
import NetworkView from '../views/NetworkView.vue'

import AdminOverview from '../views/AdminOverview.vue'
import UsersAdmin from '../views/UsersAdmin.vue'
import UserDetails from '../views/UserDetails.vue'
import StatsAdmin from '../views/AdminStats.vue'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: 
    [
      {
        path: '/network',
        name: 'network',
        component: NetworkView,
        meta: { requiresAuth: true }
      },
      {
        path: '/',
        name: 'home',
        component: HomeView,
        meta: { requiresAuth: true }
      },
      {
        path: '/files',
        name: 'files',
        component: FilesView,
        meta: { requiresAuth: true }
      },
      {
        path: '/upload',
        name: 'upload',
        component: UploadView,
        meta: { requiresAuth: true }
      },
      {
        path: '/settings',
        name: 'settings',
        component: SettingsView,
        meta: { requiresAuth: true }
      },
      {
        path: '/admin',
        name: 'admin',
        component: AdminOverview,
        meta: { requiresAuth: true }
      },
      {
        path: '/user-admin',
        name: 'user-admin',
        component: UsersAdmin,
        meta: { requiresAuth: true }
      },
      {
        path: '/admin/users/:id',
        component: UserDetails,
        meta: { requiresAuth: true }
      },
      {
        path: '/stats-admin',
        name: 'stats-admin',
        component: StatsAdmin,
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: '/',
    component: AuthLayout,
    children: 
    [
      {
        path: '/login',
        component: LoginView,
        meta: { guestOnly: true }
      },
      {
        path: '/signup',
        component: SignUpView,
        meta: { guestOnly: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {

  const auth = useAuthStore()

  /* Charger user si token existe */
  if (auth.token && !auth.user) {
    await auth.fetchUser()
  }

  /* =========================
     NON CONNECTÉ
  ========================= */

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

  /* =========================
     CONNECTÉ MAIS PAGE GUEST
  ========================= */

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return '/'
  }

})

export default router