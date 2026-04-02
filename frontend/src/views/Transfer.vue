<template>
  <div class="page transfer">
    <div class="container">
      <h1>🔄 {{ $t('transfer.title') }}</h1>

      <form @submit.prevent="handleSubmit" class="transfer-form">
        <!-- From Account -->
        <div class="form-group">
          <label class="form-label">{{ $t('transfer.from') }} *</label>
          <div class="account-selector">
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.source_account === 'cash' }"
              @click="selectSourceAccount('cash')"
            >
              <span class="account-icon">💵</span>
              <span>{{ $t('transaction.cash') }}</span>
              <span class="account-balance">{{ formatAmount(userStore.cashBalance) }}</span>
            </button>
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.source_account === 'card' }"
              @click="selectSourceAccount('card')"
            >
              <span class="account-icon">💳</span>
              <span>{{ $t('transaction.card') }}</span>
              <span class="account-balance">{{ formatAmount(userStore.cardBalance) }}</span>
            </button>
          </div>
        </div>

        <!-- Arrow Indicator -->
        <div class="transfer-arrow">
          <span>⬇️</span>
        </div>

        <!-- To Account -->
        <div class="form-group">
          <label class="form-label">{{ $t('transfer.to') }} *</label>
          <div class="account-selector">
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.destination_account === 'cash', disabled: form.source_account === 'cash' }"
              :disabled="form.source_account === 'cash'"
              @click="selectDestinationAccount('cash')"
            >
              <span class="account-icon">💵</span>
              <span>{{ $t('transaction.cash') }}</span>
            </button>
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.destination_account === 'card', disabled: form.source_account === 'card' }"
              :disabled="form.source_account === 'card'"
              @click="selectDestinationAccount('card')"
            >
              <span class="account-icon">💳</span>
              <span>{{ $t('transaction.card') }}</span>
            </button>
          </div>
        </div>

        <!-- Amount -->
        <div class="form-group">
          <label class="form-label">{{ $t('transfer.amount') }} *</label>
          <div class="amount-input-wrapper">
            <input
              v-model.number="form.amount"
              type="number"
              step="0.01"
              min="0.01"
              class="form-input amount-input"
              placeholder="0.00"
              required
              @focus="hapticFeedback('selection')"
            />
            <span class="currency-symbol">{{ currencySymbol }}</span>
          </div>
        </div>

        <!-- Date -->
        <div class="form-group">
          <label class="form-label">{{ $t('transaction.date') }}</label>
          <input
            v-model="form.date"
            type="date"
            class="form-input"
            :max="todayDate"
            @focus="hapticFeedback('selection')"
          />
        </div>

        <!-- Note -->
        <div class="form-group">
          <label class="form-label">{{ $t('transaction.note') }}</label>
          <textarea
            v-model="form.note"
            class="form-textarea"
            :placeholder="$t('transaction.addNote')"
            rows="3"
            maxlength="500"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn btn-primary btn-block"
          :disabled="loading || !isFormValid"
        >
          <span v-if="loading">{{ $t('common.loading') }}</span>
          <span v-else>🔄 {{ $t('transfer.title') }}</span>
        </button>

        <!-- Error Message -->
        <div v-if="error" class="form-error">
          {{ error }}
        </div>
      </form>
    </div>

    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useTelegram } from '../composables/useTelegram'
import { transactionAPI } from '../services/api'
import BottomNav from '../components/layout/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()
const { hapticFeedback, showAlert } = useTelegram()

const loading = ref(false)
const error = ref(null)

const form = ref({
  source_account: 'cash',
  destination_account: 'card',
  amount: null,
  date: new Date().toISOString().split('T')[0],
  note: ''
})

const currencySymbol = computed(() => {
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }
  return symbols[userStore.currency] || userStore.currency
})

const todayDate = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const isFormValid = computed(() => {
  return form.value.amount > 0 &&
         form.value.source_account &&
         form.value.destination_account &&
         form.value.source_account !== form.value.destination_account
})

const selectSourceAccount = (account) => {
  form.value.source_account = account
  // Auto-select opposite account as destination
  form.value.destination_account = account === 'cash' ? 'card' : 'cash'
  hapticFeedback('impact', 'light')
}

const selectDestinationAccount = (account) => {
  if (account !== form.value.source_account) {
    form.value.destination_account = account
    hapticFeedback('impact', 'light')
  }
}

const formatAmount = (amount) => {
  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const formatted = amount.toFixed(2)

  return currency === 'EUR' ? `${formatted} ${symbol}` : `${symbol} ${formatted}`
}

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    // Validate source balance
    const balance = form.value.source_account === 'cash'
      ? userStore.cashBalance
      : userStore.cardBalance

    if (balance < form.value.amount) {
      error.value = 'Saldo insufficiente nel conto di origine'
      hapticFeedback('notification', 'error')
      loading.value = false
      return
    }

    // Create transfer
    await transactionAPI.createTransfer({
      amount: form.value.amount,
      source_account: form.value.source_account,
      destination_account: form.value.destination_account,
      note: form.value.note || null,
      date: new Date(form.value.date).toISOString()
    })

    // Refresh balance
    await userStore.fetchBalance()

    // Success feedback
    hapticFeedback('notification', 'success')
    await showAlert('✅ Trasferimento effettuato con successo!')

    // Navigate back to dashboard
    router.push('/')

  } catch (err) {
    console.error('Error creating transfer:', err)
    error.value = err.response?.data?.detail || err.message || 'Si è verificato un errore'
    hapticFeedback('notification', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.transfer {
  padding-bottom: 80px;
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.transfer-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.transfer-arrow {
  text-align: center;
  font-size: 32px;
  margin: var(--spacing-md) 0;
}

.account-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.account-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  border: 2px solid var(--tg-theme-hint-color);
  border-radius: var(--radius-md);
  background-color: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.account-btn:not(:disabled):active {
  transform: scale(0.95);
}

.account-btn.active {
  border-color: var(--tg-theme-button-color);
  background-color: rgba(42, 171, 238, 0.1);
}

.account-btn.disabled,
.account-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.account-icon {
  font-size: 28px;
}

.account-balance {
  font-size: 12px;
  color: var(--tg-theme-hint-color);
}

.amount-input-wrapper {
  position: relative;
}

.amount-input {
  font-size: 24px;
  font-weight: 700;
  padding-right: 60px;
}

.currency-symbol {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  font-weight: 600;
  color: var(--tg-theme-hint-color);
}
</style>
