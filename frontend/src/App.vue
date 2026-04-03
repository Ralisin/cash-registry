<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <router-view />
    <DebugPanel />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useTelegram } from './composables/useTelegram'
import { useUserStore } from './stores/user'
import DebugPanel from './components/common/DebugPanel.vue'

const { colorScheme } = useTelegram()
const userStore = useUserStore()

// Dark mode computed from Telegram theme or user preference
const isDarkMode = computed(() => {
  if (userStore.user?.settings?.dark_mode !== null && userStore.user?.settings?.dark_mode !== undefined) {
    return userStore.user.settings.dark_mode
  }
  return colorScheme.value === 'dark'
})

onMounted(() => {
  // User initialization is now handled by the router guard
  // This ensures proper navigation based on user state
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
