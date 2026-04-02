<template>
  <div v-if="showDebug" class="debug-panel">
    <div class="debug-header">
      <h3>🐛 Debug Panel</h3>
      <button @click="toggleDebug" class="debug-close">✕</button>
    </div>
    <div class="debug-content">
      <div class="debug-section">
        <h4>API Configuration</h4>
        <p><strong>API URL:</strong> {{ apiUrl }}</p>
        <p><strong>Current URL:</strong> {{ currentUrl }}</p>
      </div>

      <div class="debug-section">
        <h4>Telegram WebApp</h4>
        <p><strong>Available:</strong> {{ telegramAvailable ? '✅' : '❌' }}</p>
        <p><strong>InitData:</strong> {{ initDataAvailable ? '✅' : '❌' }}</p>
        <p v-if="telegramUser"><strong>User:</strong> {{ telegramUser.first_name }} (ID: {{ telegramUser.id }})</p>
      </div>

      <div class="debug-section">
        <h4>User Store</h4>
        <p><strong>User Loaded:</strong> {{ userLoaded ? '✅' : '❌' }}</p>
        <p v-if="userStore.user"><strong>Telegram ID:</strong> {{ userStore.user.telegram_id }}</p>
        <p><strong>Balance:</strong> {{ userStore.balance ? '✅' : '❌' }}</p>
      </div>

      <div v-if="lastError" class="debug-section debug-error">
        <h4>Last Error</h4>
        <pre>{{ lastError }}</pre>
      </div>

      <div class="debug-section">
        <h4>Actions</h4>
        <button @click="testBackend" class="debug-btn">Test Backend</button>
        <button @click="initUser" class="debug-btn">Init User</button>
        <button @click="clearError" class="debug-btn">Clear Error</button>
      </div>

      <div v-if="testResult" class="debug-section">
        <h4>Test Result</h4>
        <pre>{{ testResult }}</pre>
      </div>
    </div>
  </div>
  <button v-else @click="toggleDebug" class="debug-toggle">🐛</button>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import api from '../../services/api'

const userStore = useUserStore()
const showDebug = ref(true) // Start open
const lastError = ref(null)
const testResult = ref(null)

const apiUrl = computed(() => import.meta.env.VITE_API_BASE_URL || 'NOT SET')
const currentUrl = computed(() => window.location.href)
const telegramAvailable = computed(() => !!window.Telegram?.WebApp)
const initDataAvailable = computed(() => !!window.Telegram?.WebApp?.initData)
const telegramUser = computed(() => window.Telegram?.WebApp?.initDataUnsafe?.user || null)
const userLoaded = computed(() => !!userStore.user)

const toggleDebug = () => {
  showDebug.value = !showDebug.value
}

const testBackend = async () => {
  testResult.value = 'Testing...'
  try {
    const response = await api.get('/')
    testResult.value = JSON.stringify(response.data, null, 2)
    lastError.value = null
  } catch (err) {
    lastError.value = {
      message: err.message,
      response: err.response?.data,
      status: err.response?.status,
      url: err.config?.url,
      baseURL: err.config?.baseURL
    }
    testResult.value = 'Error - see Last Error section'
  }
}

const initUser = async () => {
  testResult.value = 'Initializing user...'
  try {
    await userStore.initializeUser()
    testResult.value = 'User initialized successfully'
    lastError.value = null
  } catch (err) {
    lastError.value = {
      message: err.message,
      response: err.response?.data,
      status: err.response?.status
    }
    testResult.value = 'Error - see Last Error section'
  }
}

const clearError = () => {
  lastError.value = null
  testResult.value = null
}

// Capture global errors
onMounted(() => {
  window.addEventListener('unhandledrejection', (event) => {
    lastError.value = {
      type: 'Unhandled Promise Rejection',
      message: event.reason?.message || event.reason,
      stack: event.reason?.stack
    }
  })

  window.addEventListener('error', (event) => {
    lastError.value = {
      type: 'Error',
      message: event.message,
      filename: event.filename,
      lineno: event.lineno
    }
  })
})
</script>

<style scoped>
.debug-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  color: #0f0;
  font-family: monospace;
  font-size: 12px;
  z-index: 9999;
  overflow-y: auto;
  padding: 20px;
}

.debug-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #0f0;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.debug-header h3 {
  margin: 0;
  color: #0f0;
}

.debug-close {
  background: none;
  border: 1px solid #0f0;
  color: #0f0;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 16px;
}

.debug-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.debug-section {
  border: 1px solid #0f0;
  padding: 10px;
  border-radius: 4px;
}

.debug-section h4 {
  margin: 0 0 10px 0;
  color: #ff0;
}

.debug-section p {
  margin: 5px 0;
  word-break: break-all;
}

.debug-error {
  border-color: #f00;
  background: rgba(255, 0, 0, 0.1);
}

.debug-error h4 {
  color: #f00;
}

.debug-error pre {
  color: #f00;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 10px 0 0 0;
}

.debug-btn {
  background: #0f0;
  color: #000;
  border: none;
  padding: 8px 12px;
  margin: 5px 5px 5px 0;
  cursor: pointer;
  border-radius: 4px;
  font-weight: bold;
}

.debug-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0f0;
  color: #000;
  border: none;
  font-size: 24px;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

pre {
  color: #0f0;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 10px 0 0 0;
}
</style>
