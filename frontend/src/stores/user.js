/**
 * User Store (Pinia)
 * Manages user state and authentication
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userAPI } from '../services/api'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const balance = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const telegramId = computed(() => user.value?.telegram_id || null)
  const userName = computed(() => user.value?.name || 'User')
  const currency = computed(() => user.value?.settings?.currency || 'EUR')
  const language = computed(() => user.value?.settings?.language || 'it')

  const totalBalance = computed(() => {
    if (!balance.value) return 0
    return balance.value.total_balance
  })

  const cashBalance = computed(() => {
    if (!balance.value) return 0
    return balance.value.cash_balance
  })

  const cardBalance = computed(() => {
    if (!balance.value) return 0
    return balance.value.card_balance
  })

  // Actions
  async function initializeUser() {
    loading.value = true
    error.value = null

    try {
      // Get initData from Telegram
      const initData = window.Telegram?.WebApp?.initData
      if (!initData) {
        throw new Error('Telegram initData not available')
      }

      // Register or get user
      const response = await userAPI.createUser(initData)
      user.value = response.data

      // Get balance
      await fetchBalance()

      return user.value
    } catch (err) {
      error.value = err.message
      console.error('Error initializing user:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!user.value?.telegram_id) return

    loading.value = true
    error.value = null

    try {
      const response = await userAPI.getUser(user.value.telegram_id)
      user.value = response.data
      return user.value
    } catch (err) {
      error.value = err.message
      console.error('Error fetching user:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchBalance() {
    if (!user.value?.telegram_id) return

    try {
      const response = await userAPI.getBalance(user.value.telegram_id)
      balance.value = response.data
      return balance.value
    } catch (err) {
      console.error('Error fetching balance:', err)
      throw err
    }
  }

  async function updateSettings(settings) {
    if (!user.value?.telegram_id) return

    loading.value = true
    error.value = null

    try {
      const response = await userAPI.updateSettings(user.value.telegram_id, settings)
      user.value = response.data
      return user.value
    } catch (err) {
      error.value = err.message
      console.error('Error updating settings:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function initializeBalance(data) {
    if (!user.value?.telegram_id) return

    loading.value = true
    error.value = null

    try {
      const response = await userAPI.initializeBalance(user.value.telegram_id, data)
      balance.value = response.data
      return balance.value
    } catch (err) {
      error.value = err.message
      console.error('Error initializing balance:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateBalance(data) {
    if (!user.value?.telegram_id) return

    loading.value = true
    error.value = null

    try {
      const response = await userAPI.updateBalance(user.value.telegram_id, data)
      balance.value = response.data
      return balance.value
    } catch (err) {
      error.value = err.message
      console.error('Error updating balance:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    balance.value = null
    error.value = null
  }

  return {
    // State
    user,
    balance,
    loading,
    error,
    // Getters
    isAuthenticated,
    telegramId,
    userName,
    currency,
    language,
    totalBalance,
    cashBalance,
    cardBalance,
    // Actions
    initializeUser,
    fetchUser,
    fetchBalance,
    updateSettings,
    initializeBalance,
    updateBalance,
    logout
  }
})
