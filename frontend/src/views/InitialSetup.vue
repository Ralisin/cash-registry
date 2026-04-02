<template>
  <div class="page setup">
    <div class="container">
      <div class="setup-card">
        <!-- Header -->
        <div class="setup-header">
          <span class="setup-icon">🏕️</span>
          <h1>{{ $t('setup.welcome') }}</h1>
          <p class="setup-description">{{ $t('setup.description') }}</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="setup-form">
          <!-- Cash Balance -->
          <div class="form-group">
            <label class="form-label">
              💵 {{ $t('setup.cashBalance') }}
            </label>
            <input
              v-model.number="form.cashBalance"
              type="number"
              step="0.01"
              min="0"
              class="form-input"
              :placeholder="'0.00'"
              required
            />
          </div>

          <!-- Card Balance -->
          <div class="form-group">
            <label class="form-label">
              💳 {{ $t('setup.cardBalance') }}
            </label>
            <input
              v-model.number="form.cardBalance"
              type="number"
              step="0.01"
              min="0"
              class="form-input"
              :placeholder="'0.00'"
              required
            />
          </div>

          <!-- Total Display -->
          <div class="total-display">
            <span class="total-label">{{ $t('dashboard.totalBalance') }}</span>
            <span class="total-amount">{{ formattedTotal }}</span>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary btn-block"
            :disabled="loading"
          >
            <span v-if="loading">{{ $t('common.loading') }}</span>
            <span v-else>{{ $t('setup.continue') }}</span>
          </button>

          <!-- Error Message -->
          <div v-if="error" class="form-error">
            {{ error }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useTelegram } from '../composables/useTelegram'

const router = useRouter()
const userStore = useUserStore()
const { hapticFeedback, showAlert } = useTelegram()

const loading = ref(false)
const error = ref(null)

const form = ref({
  cashBalance: 0,
  cardBalance: 0
})

const formattedTotal = computed(() => {
  const total = (form.value.cashBalance || 0) + (form.value.cardBalance || 0)
  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const formatted = total.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

  return currency === 'EUR' ? `${formatted} ${symbol}` : `${symbol} ${formatted}`
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    // Check if user is initialized
    if (!userStore.user?.telegram_id) {
      console.log('User not initialized, attempting to initialize...')
      await userStore.initializeUser()
    }

    // Check again after initialization
    if (!userStore.user?.telegram_id) {
      throw new Error('User initialization failed. Please refresh the page.')
    }

    // Initialize balance
    console.log('Initializing balance with:', {
      cash_balance: form.value.cashBalance,
      card_balance: form.value.cardBalance
    })

    await userStore.initializeBalance({
      cash_balance: form.value.cashBalance,
      card_balance: form.value.cardBalance
    })

    console.log('Balance initialized successfully')

    // Success feedback
    hapticFeedback('notification', 'success')

    // Navigate to dashboard
    router.push('/')

  } catch (err) {
    console.error('Error initializing balance:', err)
    error.value = err.response?.data?.detail || err.message || 'Si è verificato un errore'
    hapticFeedback('notification', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.setup {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, var(--tg-theme-button-color) 0%, var(--tg-theme-bg-color) 100%);
}

.setup-card {
  width: 100%;
  max-width: 500px;
  background-color: var(--tg-theme-bg-color);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-lg);
}

.setup-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.setup-icon {
  font-size: 64px;
  display: block;
  margin-bottom: var(--spacing-md);
}

.setup-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.setup-description {
  color: var(--tg-theme-hint-color);
  font-size: 15px;
  line-height: 1.5;
}

.setup-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.total-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background-color: var(--tg-theme-secondary-bg-color);
  border-radius: var(--radius-md);
  margin: var(--spacing-sm) 0;
}

.total-label {
  font-weight: 600;
  color: var(--tg-theme-hint-color);
}

.total-amount {
  font-size: 24px;
  font-weight: 700;
  color: var(--tg-theme-button-color);
}
</style>
