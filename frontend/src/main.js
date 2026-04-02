/**
 * Scout Finance App - Main Entry Point
 * Vue 3 + Composition API
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

// Import global styles
import './assets/styles/main.css'

// Create Vue app
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)
app.use(i18n)

// Mount app
app.mount('#app')

// Initialize Telegram Web App
if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.ready()
  window.Telegram.WebApp.expand()
}
