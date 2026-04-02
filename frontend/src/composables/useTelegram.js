/**
 * Telegram Web App Composable
 * Provides access to Telegram Web App SDK functionality
 */

import { ref, computed, onMounted, markRaw } from 'vue'

export function useTelegram() {
  const webApp = ref(null)
  const initDataUnsafe = ref(null)
  const initData = ref(null)

  onMounted(() => {
    if (window.Telegram?.WebApp) {
      // Use markRaw to prevent Vue from making Telegram WebApp reactive
      // This avoids proxy errors with read-only properties like HapticFeedback
      webApp.value = markRaw(window.Telegram.WebApp)
      initDataUnsafe.value = webApp.value.initDataUnsafe
      initData.value = webApp.value.initData
    }
  })

  // Computed properties
  const user = computed(() => initDataUnsafe.value?.user || null)
  const colorScheme = computed(() => webApp.value?.colorScheme || 'light')
  const themeParams = computed(() => webApp.value?.themeParams || {})
  const isExpanded = computed(() => webApp.value?.isExpanded || false)

  // Methods
  const showBackButton = () => {
    if (webApp.value) {
      webApp.value.BackButton.show()
    }
  }

  const hideBackButton = () => {
    if (webApp.value) {
      webApp.value.BackButton.hide()
    }
  }

  const showMainButton = (text, onClick) => {
    if (webApp.value) {
      webApp.value.MainButton.setText(text)
      webApp.value.MainButton.onClick(onClick)
      webApp.value.MainButton.show()
    }
  }

  const hideMainButton = () => {
    if (webApp.value) {
      webApp.value.MainButton.hide()
    }
  }

  const enableMainButton = () => {
    if (webApp.value) {
      webApp.value.MainButton.enable()
    }
  }

  const disableMainButton = () => {
    if (webApp.value) {
      webApp.value.MainButton.disable()
    }
  }

  const showAlert = (message) => {
    if (webApp.value) {
      webApp.value.showAlert(message)
    } else {
      alert(message)
    }
  }

  const showConfirm = (message) => {
    return new Promise((resolve) => {
      if (webApp.value) {
        webApp.value.showConfirm(message, resolve)
      } else {
        resolve(confirm(message))
      }
    })
  }

  const hapticFeedback = (type = 'impact', style = 'medium') => {
    if (webApp.value?.HapticFeedback) {
      if (type === 'impact') {
        webApp.value.HapticFeedback.impactOccurred(style)
      } else if (type === 'notification') {
        webApp.value.HapticFeedback.notificationOccurred(style)
      } else if (type === 'selection') {
        webApp.value.HapticFeedback.selectionChanged()
      }
    }
  }

  const expand = () => {
    if (webApp.value) {
      webApp.value.expand()
    }
  }

  const close = () => {
    if (webApp.value) {
      webApp.value.close()
    }
  }

  return {
    webApp,
    initData,
    initDataUnsafe,
    user,
    colorScheme,
    themeParams,
    isExpanded,
    showBackButton,
    hideBackButton,
    showMainButton,
    hideMainButton,
    enableMainButton,
    disableMainButton,
    showAlert,
    showConfirm,
    hapticFeedback,
    expand,
    close
  }
}
