import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import FilesView from '../views/FilesView.vue'
import UploadView from '../views/UploadView.vue'
import SettingsView from '../views/SettingsView.vue'
import NetworkView from '../views/NetworkView.vue'

const routes = [
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
]

export default createRouter({
  history: createWebHistory(),
  routes,
})