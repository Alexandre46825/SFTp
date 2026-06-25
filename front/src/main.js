import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

createApp(App)
  .use(router)
  .use(createPinia())
  .mount('#app')

const userStore = useUserStore()
const themeStore = useThemeStore()

themeStore.initializeTheme()

if (localStorage.getItem('token')) {
  userStore.loadProfile()
}

