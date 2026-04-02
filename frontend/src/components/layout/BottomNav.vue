<template>
  <nav class="bottom-nav">
    <router-link
      v-for="item in navItems"
      :key="item.name"
      :to="item.path"
      class="nav-item"
      :class="{ active: isActive(item.path) }"
      @click="hapticFeedback"
    >
      <span class="nav-icon">{{ item.icon }}</span>
      <span class="nav-label">{{ $t(item.label) }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTelegram } from '../../composables/useTelegram'

const route = useRoute()
const { hapticFeedback } = useTelegram()

const navItems = [
  { name: 'dashboard', path: '/', icon: '📊', label: 'nav.dashboard' },
  { name: 'add', path: '/add-transaction', icon: '➕', label: 'nav.addTransaction' },
  { name: 'history', path: '/history', icon: '📜', label: 'nav.history' },
  { name: 'analytics', path: '/analytics', icon: '📈', label: 'nav.analytics' },
  { name: 'settings', path: '/settings', icon: '⚙️', label: 'nav.settings' }
]

const isActive = (path) => {
  return route.path === path
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: var(--tg-theme-secondary-bg-color);
  border-top: 1px solid var(--tg-theme-hint-color);
  padding: 8px 0;
  z-index: 100;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  text-decoration: none;
  color: var(--tg-theme-hint-color);
  transition: all var(--transition-fast);
  min-width: 60px;
}

.nav-item:hover,
.nav-item.active {
  color: var(--tg-theme-button-color);
}

.nav-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.nav-label {
  font-size: 11px;
  font-weight: 500;
  text-align: center;
}
</style>
