<template>
  <div class="transaction-item" @click="$emit('click', transaction)">
    <div class="transaction-icon" :class="transaction.type">
      {{ typeIcon }}
    </div>
    <div class="transaction-details">
      <div class="transaction-category">{{ transaction.category_name }}</div>
      <div class="transaction-info">
        <span class="transaction-account">{{ accountLabel }}</span>
        <span class="transaction-date">{{ formattedDate }}</span>
      </div>
      <div v-if="transaction.note" class="transaction-note">{{ transaction.note }}</div>
    </div>
    <div class="transaction-amount" :class="amountClass">
      {{ formattedAmount }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '../../stores/user'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

const userStore = useUserStore()
const { t } = useI18n()

const typeIcon = computed(() => {
  const icons = {
    expense: '💸',
    income: '💰',
    transfer: '🔄'
  }
  return icons[props.transaction.type] || '📝'
})

const amountClass = computed(() => {
  return props.transaction.type === 'expense' ? 'negative' : 'positive'
})

const accountLabel = computed(() => {
  const account = props.transaction.source_account
  return t(`transaction.${account}`)
})

const formattedAmount = computed(() => {
  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const amount = Math.abs(props.transaction.amount)
  const formatted = amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

  const sign = props.transaction.type === 'expense' ? '-' : '+'

  return currency === 'EUR'
    ? `${sign}${formatted} ${symbol}`
    : `${sign}${symbol} ${formatted}`
})

const formattedDate = computed(() => {
  const date = new Date(props.transaction.date)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return t('common.today') || 'Oggi'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return t('common.yesterday') || 'Ieri'
  } else {
    return date.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' })
  }
})
</script>

<style scoped>
.transaction-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--tg-theme-secondary-bg-color);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.transaction-item:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}

.transaction-item:active {
  transform: scale(0.98);
}

.transaction-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.transaction-icon.expense {
  background-color: rgba(244, 67, 54, 0.1);
}

.transaction-icon.income {
  background-color: rgba(76, 175, 80, 0.1);
}

.transaction-icon.transfer {
  background-color: rgba(33, 150, 243, 0.1);
}

.transaction-details {
  flex: 1;
  min-width: 0;
}

.transaction-category {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.transaction-info {
  display: flex;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--tg-theme-hint-color);
}

.transaction-note {
  font-size: 13px;
  color: var(--tg-theme-hint-color);
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.transaction-amount {
  font-size: 18px;
  font-weight: 700;
  white-space: nowrap;
}

.transaction-amount.negative {
  color: var(--color-expense);
}

.transaction-amount.positive {
  color: var(--color-income);
}
</style>
