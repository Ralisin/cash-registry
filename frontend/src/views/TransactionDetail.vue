<template>
  <div class="page transaction-detail">
    <div class="container">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
      </div>

      <div v-else-if="transaction" class="detail-content">
        <!-- Transaction Header -->
        <div class="transaction-header" :class="transaction.type">
          <span class="transaction-icon-large">{{ typeIcon }}</span>
          <h1 class="transaction-amount-large">{{ formattedAmount }}</h1>
          <span class="transaction-type-label">{{ typeLabel }}</span>
        </div>

        <!-- Transaction Details -->
        <div class="detail-card">
          <div class="detail-row">
            <span class="detail-label">{{ $t('transaction.category') }}</span>
            <span class="detail-value">{{ transaction.category_name }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">{{ $t('transaction.account') }}</span>
            <span class="detail-value">
              {{ transaction.source_account === 'cash' ? '💵 ' + $t('transaction.cash') : '💳 ' + $t('transaction.card') }}
            </span>
          </div>

          <div v-if="transaction.destination_account" class="detail-row">
            <span class="detail-label">A</span>
            <span class="detail-value">
              {{ transaction.destination_account === 'cash' ? '💵 ' + $t('transaction.cash') : '💳 ' + $t('transaction.card') }}
            </span>
          </div>

          <div class="detail-row">
            <span class="detail-label">{{ $t('transaction.date') }}</span>
            <span class="detail-value">{{ formattedDate }}</span>
          </div>

          <div v-if="transaction.note" class="detail-row">
            <span class="detail-label">{{ $t('transaction.note') }}</span>
            <span class="detail-value note">{{ transaction.note }}</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button
            v-if="transaction.type !== 'transfer'"
            class="btn btn-secondary btn-block"
            @click="handleEdit"
          >
            ✏️ {{ $t('common.edit') }}
          </button>
          <button
            class="btn btn-danger btn-block"
            @click="handleDelete"
            :disabled="deleting"
          >
            <span v-if="deleting">{{ $t('common.loading') }}</span>
            <span v-else>🗑️ {{ $t('common.delete') }}</span>
          </button>
        </div>
      </div>

      <div v-else class="error-state">
        <span class="error-icon">❌</span>
        <p>Transazione non trovata</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '../stores/user'
import { useTelegram } from '../composables/useTelegram'
import { transactionAPI } from '../services/api'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const userStore = useUserStore()
const { hapticFeedback, showConfirm, showAlert } = useTelegram()

const loading = ref(true)
const deleting = ref(false)
const transaction = ref(null)
const error = ref(null)

onMounted(async () => {
  await loadTransaction()
})

const loadTransaction = async () => {
  loading.value = true
  try {
    const response = await transactionAPI.getTransaction(route.params.id)
    transaction.value = response.data
  } catch (err) {
    console.error('Error loading transaction:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const typeIcon = computed(() => {
  const icons = {
    expense: '💸',
    income: '💰',
    transfer: '🔄'
  }
  return icons[transaction.value?.type] || '📝'
})

const typeLabel = computed(() => {
  return t(`transaction.${transaction.value?.type}`)
})

const formattedAmount = computed(() => {
  if (!transaction.value) return ''

  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const amount = Math.abs(transaction.value.amount)
  const formatted = amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

  const sign = transaction.value.type === 'expense' ? '-' : '+'

  return currency === 'EUR'
    ? `${sign}${formatted} ${symbol}`
    : `${sign}${symbol} ${formatted}`
})

const formattedDate = computed(() => {
  if (!transaction.value) return ''

  const date = new Date(transaction.value.date)
  return date.toLocaleDateString('it-IT', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const handleEdit = () => {
  // TODO: Implement edit functionality
  showAlert('Funzionalità in arrivo')
}

const handleDelete = async () => {
  hapticFeedback('impact', 'medium')

  const confirmed = await showConfirm(
    t('transaction.deleteConfirm') + '\n\n' + t('transaction.deleteWarning')
  )

  if (!confirmed) return

  deleting.value = true

  try {
    await transactionAPI.deleteTransaction(transaction.value.id)

    // Refresh balance
    await userStore.fetchBalance()

    // Success feedback
    hapticFeedback('notification', 'success')
    await showAlert('✅ Transazione eliminata')

    // Navigate back
    router.push('/')

  } catch (err) {
    console.error('Error deleting transaction:', err)
    hapticFeedback('notification', 'error')
    await showAlert('❌ Errore durante l\'eliminazione')
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
.transaction-detail {
  min-height: 100vh;
  padding-bottom: var(--spacing-xl);
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.transaction-header {
  text-align: center;
  padding: var(--spacing-xl) 0;
  margin-bottom: var(--spacing-lg);
  border-radius: var(--radius-xl);
}

.transaction-header.expense {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(244, 67, 54, 0.05) 100%);
}

.transaction-header.income {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
}

.transaction-header.transfer {
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(33, 150, 243, 0.05) 100%);
}

.transaction-icon-large {
  font-size: 64px;
  display: block;
  margin-bottom: var(--spacing-md);
}

.transaction-amount-large {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 var(--spacing-sm) 0;
}

.transaction-type-label {
  font-size: 16px;
  color: var(--tg-theme-hint-color);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.detail-card {
  background-color: var(--tg-theme-secondary-bg-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 14px;
  color: var(--tg-theme-hint-color);
  font-weight: 500;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  text-align: right;
  max-width: 60%;
}

.detail-value.note {
  font-weight: 400;
  white-space: pre-wrap;
  word-break: break-word;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.error-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
}
</style>
