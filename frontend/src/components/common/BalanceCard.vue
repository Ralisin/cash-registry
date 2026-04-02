<template>
  <div class="balance-card" :class="variant">
    <div class="balance-header">
      <span class="balance-icon">{{ icon }}</span>
      <span class="balance-title">{{ title }}</span>
    </div>
    <div class="balance-amount">{{ formattedAmount }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '../../stores/user'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  icon: {
    type: String,
    default: '💰'
  },
  variant: {
    type: String,
    default: 'default', // default, primary, success
    validator: (value) => ['default', 'primary', 'success'].includes(value)
  }
})

const userStore = useUserStore()

const formattedAmount = computed(() => {
  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const formatted = props.amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

  return currency === 'EUR' ? `${formatted} ${symbol}` : `${symbol} ${formatted}`
})
</script>

<style scoped>
.balance-card {
  background: linear-gradient(135deg, var(--tg-theme-secondary-bg-color) 0%, var(--tg-theme-bg-color) 100%);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-md);
  transition: transform var(--transition-fast);
}

.balance-card:active {
  transform: scale(0.98);
}

.balance-card.primary {
  background: linear-gradient(135deg, #2AABEE 0%, #229ED9 100%);
  color: white;
}

.balance-card.success {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.balance-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
  font-size: 14px;
  opacity: 0.9;
}

.balance-icon {
  font-size: 20px;
}

.balance-title {
  font-weight: 500;
}

.balance-amount {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

@media (max-width: 768px) {
  .balance-amount {
    font-size: 24px;
  }
}
</style>
