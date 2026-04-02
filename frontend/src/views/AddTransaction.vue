<template>
  <div class="page add-transaction">
    <div class="container">
      <!-- Type Selector -->
      <div class="type-selector">
        <button
          class="type-btn"
          :class="{ active: form.type === 'expense' }"
          @click="selectType('expense')"
        >
          <span class="type-icon">💸</span>
          <span>{{ $t('transaction.expense') }}</span>
        </button>
        <button
          class="type-btn"
          :class="{ active: form.type === 'income' }"
          @click="selectType('income')"
        >
          <span class="type-icon">💰</span>
          <span>{{ $t('transaction.income') }}</span>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="transaction-form">
        <!-- Amount -->
        <div class="form-group">
          <label class="form-label">{{ $t('transaction.amount') }} *</label>
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

        <!-- Category -->
        <div class="form-group">
          <label class="form-label">{{ $t('transaction.category') }} *</label>
          <select
            v-model="form.category_id"
            class="form-select"
            required
            @change="hapticFeedback('selection')"
          >
            <option value="" disabled>{{ $t('transaction.selectCategory') }}</option>
            <option
              v-for="category in categoriesStore.categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.icon ? `${category.icon} ` : '' }}{{ category.name }}
            </option>
          </select>
        </div>

        <!-- Account -->
        <div class="form-group">
          <label class="form-label">{{ $t('transaction.account') }} *</label>
          <div class="account-selector">
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.source_account === 'cash' }"
              @click="selectAccount('cash')"
            >
              <span class="account-icon">💵</span>
              <span>{{ $t('transaction.cash') }}</span>
              <span class="account-balance">{{ formatAmount(userStore.cashBalance) }}</span>
            </button>
            <button
              type="button"
              class="account-btn"
              :class="{ active: form.source_account === 'card' }"
              @click="selectAccount('card')"
            >
              <span class="account-icon">💳</span>
              <span>{{ $t('transaction.card') }}</span>
              <span class="account-balance">{{ formatAmount(userStore.cardBalance) }}</span>
            </button>
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
          <span v-else>
            {{ form.type === 'expense' ? '💸' : '💰' }}
            {{ form.type === 'expense' ? $t('transaction.expense') : $t('transaction.income') }}
          </span>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useCategoriesStore } from '../stores/categories'
import { useTelegram } from '../composables/useTelegram'
import { transactionAPI } from '../services/api'
import BottomNav from '../components/layout/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()
const categoriesStore = useCategoriesStore()
const { hapticFeedback, showAlert } = useTelegram()

const loading = ref(false)
const error = ref(null)

const form = ref({
  type: 'expense',
  amount: null,
  category_id: '',
  source_account: 'cash',
  date: new Date().toISOString().split('T')[0],
  note: ''
})

onMounted(async () => {
  // Load categories
  if (categoriesStore.categories.length === 0) {
    await categoriesStore.fetchCategories()
  }
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
         form.value.category_id &&
         form.value.source_account
})

const selectType = (type) => {
  form.value.type = type
  hapticFeedback('impact', 'light')
}

const selectAccount = (account) => {
  form.value.source_account = account
  hapticFeedback('impact', 'light')
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
    // Validate balance for expenses
    if (form.value.type === 'expense') {
      const balance = form.value.source_account === 'cash'
        ? userStore.cashBalance
        : userStore.cardBalance

      if (balance < form.value.amount) {
        error.value = 'Saldo insufficiente'
        hapticFeedback('notification', 'error')
        loading.value = false
        return
      }
    }

    // Create transaction
    await transactionAPI.createTransaction({
      amount: form.value.amount,
      type: form.value.type,
      source_account: form.value.source_account,
      category_id: form.value.category_id,
      note: form.value.note || null,
      date: new Date(form.value.date).toISOString()
    })

    // Refresh balance
    await userStore.fetchBalance()

    // Success feedback
    hapticFeedback('notification', 'success')
    await showAlert('✅ Transazione creata con successo!')

    // Navigate back to dashboard
    router.push('/')

  } catch (err) {
    console.error('Error creating transaction:', err)
    error.value = err.response?.data?.detail || err.message || 'Si è verificato un errore'
    hapticFeedback('notification', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-transaction {
  padding-bottom: 80px;
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.type-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg) var(--spacing-md);
  border: 2px solid var(--tg-theme-hint-color);
  border-radius: var(--radius-lg);
  background-color: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.type-btn:active {
  transform: scale(0.95);
}

.type-btn.active {
  border-color: var(--tg-theme-button-color);
  background-color: var(--tg-theme-button-color);
  color: white;
}

.type-icon {
  font-size: 32px;
}

.transaction-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
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

.account-btn:active {
  transform: scale(0.95);
}

.account-btn.active {
  border-color: var(--tg-theme-button-color);
  background-color: rgba(42, 171, 238, 0.1);
}

.account-icon {
  font-size: 28px;
}

.account-balance {
  font-size: 12px;
  color: var(--tg-theme-hint-color);
}
</style>
