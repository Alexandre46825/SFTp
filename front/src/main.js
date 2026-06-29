import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/Auth'

createApp(App)
  .use(router)
  .use(createPinia())
  .mount('#app')

const authStore = useAuthStore()

if (localStorage.getItem('token')) {
  authStore.fetchUser()
}

