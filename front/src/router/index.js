import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/Auth'

import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import HomeView from '../views/HomeView.vue'

import UploadView from '../views/UploadView.vue'
import DownloadView from '../views/DownloadView.vue'
import SettingsView from '../views/SettingsView.vue'
import NetworkView from '../views/NetworkView.vue'

import AdminOverview from '../views/AdminOverview.vue'
import UsersAdmin from '../views/UsersAdmin.vue'
import UserDetails from '../views/UserDetails.vue'
import LogsView from '../views/LogsView.vue'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

/* =========================
   ROUTES
========================= */
const routes = [

  /* =========================
     APP (AUTH REQUIRED)
  ========================= */
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
        meta: { requiresAuth: true }
      },
      {
        path: 'network',
        name: 'network',
        component: NetworkView,
        meta: { requiresAuth: true }
      },
      {
        path: 'upload',
        name: 'upload',
        component: UploadView,
        meta: { requiresAuth: true }
      },
      {
        path: 'download/:id_file',
        name: 'download',
        component: DownloadView,
        meta: { requiresAuth: true }
      },
      {
        path: 'settings',
        name: 'settings',
        component: SettingsView,
        meta: { requiresAuth: true }
      },

      /* =========================
         ADMIN ROUTES
      ========================= */
      {
        path: 'admin',
        name: 'admin',
        component: AdminOverview,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/users',
        name: 'admin-users',
        component: UsersAdmin,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/users/:id',
        name: 'admin-user-details',
        component: UserDetails,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'admin/logs',
        name: 'admin-logs',
        component: LogsView,
        meta: { requiresAuth: true, requiresAdmin: true }
      }
    ]
  },

  /* =========================
     AUTH
  ========================= */
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'login',
        component: LoginView,
        meta: { guestOnly: true }
      },
      {
        path: 'signup',
        name: 'signup',
        component: SignUpView,
        meta: { guestOnly: true }
      }
    ]
  }
]

/* =========================
   ROUTER
========================= */
const router = createRouter({
  history: createWebHistory(),
  routes
})

/* =========================
   GLOBAL GUARD
========================= */
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // charge user si token existe
  if (auth.token && !auth.user) {
    await auth.fetchUser()
  }

  // pas connecté
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

  // connecté mais page login/signup
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return '/'
  }

  // admin only
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return '/'
  }
})

export default router