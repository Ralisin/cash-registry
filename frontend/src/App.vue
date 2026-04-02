<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <router-view />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useTelegram } from './composables/useTelegram'
import { useUserStore } from './stores/user'

const { colorScheme } = useTelegram()
const userStore = useUserStore()

// Dark mode computed from Telegram theme or user preference
const isDarkMode = computed(() => {
  if (userStore.user?.settings?.dark_mode !== null && userStore.user?.settings?.dark_mode !== undefined) {
    return userStore.user.settings.dark_mode
  }
  return colorScheme.value === 'dark'
})

onMounted(async () => {
  // Initialize user from Telegram
  try {
    console.log('Initializing user from Telegram...')
    await userStore.initializeUser()
    console.log('User initialized successfully:', userStore.user)
  } catch (err) {
    console.error('Failed to initialize user:', err)
    // Don't block the app, user will be initialized when clicking Continue
  }
})
</script>

<style>
/* Global styles are in assets/styles/main.css */
#app {
  min-height: 100vh;
  background-color: var(--tg-theme-bg-color, #ffffff);
  color: var(--tg-theme-text-color, #000000);
  transition: background-color 0.3s, color 0.3s;
}

#app.dark-mode {
  background-color: var(--tg-theme-bg-color, #212121);
  color: var(--tg-theme-text-color, #ffffff);
}
</style>
