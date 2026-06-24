import { createRouter, createWebHistory } from 'vue-router'

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
      },
      {
        path: '/',
        name: 'home',
        component: HomeView,
      },
      {
        path: '/files',
        name: 'files',
        component: FilesView,
      },
      {
        path: '/upload',
        name: 'upload',
        component: UploadView,
      },
      {
        path: '/settings',
        name: 'settings',
        component: SettingsView,
      },
      {
        path: '/admin',
        name: 'admin',
        component: AdminOverview,
      },
      {
        path: '/user-admin',
        name: 'user-admin',
        component: UsersAdmin,
      },
      {
        path: '/admin/users/:id',
        component: UserDetails,
      },
      {
        path: '/stats-admin',
        name: 'stats-admin',
        component: StatsAdmin,
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
        component: LoginView
      },
      {
        path: '/signup',
        component: SignUpView
      }
    ]
  }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})