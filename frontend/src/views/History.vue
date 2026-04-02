<template>
  <div class="page history">
    <div class="container">
      <h1>{{ $t('history.title') }}</h1>

      <!-- Filters -->
      <div class="filters-section">
        <!-- Type Filter -->
        <div class="filter-tabs">
          <button
            v-for="type in filterTypes"
            :key="type.value"
            class="filter-tab"
            :class="{ active: filters.type === type.value }"
            @click="selectType(type.value)"
          >
            {{ type.label }}
          </button>
        </div>

        <!-- Date Range Filter -->
        <div class="date-filters">
          <button
            v-for="range in dateRanges"
            :key="range.value"
            class="date-btn"
            :class="{ active: selectedRange === range.value }"
            @click="selectDateRange(range.value)"
          >
            {{ range.label }}
          </button>
        </div>

        <!-- Custom Date Range -->
        <div v-if="selectedRange === 'custom'" class="custom-date-range">
          <input
            v-model="filters.start_date"
            type="date"
            class="form-input"
            @change="loadTransactions"
          />
          <span>→</span>
          <input
            v-model="filters.end_date"
            type="date"
            class="form-input"
            @change="loadTransactions"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
      </div>

      <!-- Transaction List -->
      <div v-else-if="transactions.length > 0" class="transactions-container">
        <div class="transactions-summary">
          <span>{{ transactions.length }} transazioni</span>
        </div>

        <div class="transactions-list">
          <TransactionItem
            v-for="transaction in transactions"
            :key="transaction.id"
            :transaction="transaction"
            @click="goToDetail(transaction)"
          />
        </div>

        <!-- Load More (if needed) -->
        <button
          v-if="hasMore"
          class="btn btn-secondary btn-block mt-md"
          @click="loadMore"
          :disabled="loadingMore"
        >
          <span v-if="loadingMore">{{ $t('common.loading') }}</span>
          <span v-else">Carica altro</span>
        </button>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <span class="empty-icon">📝</span>
        <p>{{ $t('history.noResults') }}</p>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useTelegram } from '../composables/useTelegram'
import { transactionAPI } from '../services/api'
import TransactionItem from '../components/transaction/TransactionItem.vue'
import BottomNav from '../components/layout/BottomNav.vue'

const router = useRouter()
const { t } = useI18n()
const { hapticFeedback } = useTelegram()

const loading = ref(true)
const loadingMore = ref(false)
const transactions = ref([])
const hasMore = ref(false)
const selectedRange = ref('all')

const filters = ref({
  type: null,
  start_date: null,
  end_date: null,
  limit: 50,
  skip: 0
})

const filterTypes = computed(() => [
  { value: null, label: t('history.all') },
  { value: 'expense', label: t('history.expenses') },
  { value: 'income', label: t('history.income') },
  { value: 'transfer', label: t('history.transfers') }
])

const dateRanges = computed(() => {
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth()

  // Scout year: September to June
  let scoutYearStart
  let scoutYearEnd

  if (currentMonth >= 8) { // September or later
    scoutYearStart = new Date(currentYear, 8, 1) // September 1st
    scoutYearEnd = new Date(currentYear + 1, 5, 30) // June 30th next year
  } else { // Before September
    scoutYearStart = new Date(currentYear - 1, 8, 1)
    scoutYearEnd = new Date(currentYear, 5, 30)
  }

  return [
    { value: 'all', label: 'Tutte' },
    {
      value: 'scout_year',
      label: 'Anno Scout',
      start: scoutYearStart.toISOString().split('T')[0],
      end: scoutYearEnd.toISOString().split('T')[0]
    },
    {
      value: 'month',
      label: 'Ultimo Mese',
      start: new Date(now.getFullYear(), now.getMonth() - 1, now.getDate()).toISOString().split('T')[0],
      end: now.toISOString().split('T')[0]
    },
    {
      value: 'week',
      label: 'Ultima Settimana',
      start: new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      end: now.toISOString().split('T')[0]
    },
    { value: 'custom', label: 'Custom' }
  ]
})

onMounted(() => {
  loadTransactions()
})

const selectType = (type) => {
  filters.value.type = type
  filters.value.skip = 0
  hapticFeedback('selection')
  loadTransactions()
}

const selectDateRange = (range) => {
  selectedRange.value = range
  filters.value.skip = 0

  const rangeData = dateRanges.value.find(r => r.value === range)

  if (range === 'all') {
    filters.value.start_date = null
    filters.value.end_date = null
  } else if (range !== 'custom' && rangeData) {
    filters.value.start_date = rangeData.start
    filters.value.end_date = rangeData.end
  }

  if (range !== 'custom') {
    hapticFeedback('selection')
    loadTransactions()
  }
}

const loadTransactions = async () => {
  loading.value = true

  try {
    const params = {
      limit: filters.value.limit,
      skip: filters.value.skip
    }

    if (filters.value.type) {
      params.type = filters.value.type
    }

    if (filters.value.start_date) {
      params.start_date = new Date(filters.value.start_date).toISOString()
    }

    if (filters.value.end_date) {
      params.end_date = new Date(filters.value.end_date).toISOString()
    }

    const response = await transactionAPI.getTransactions(params)
    transactions.value = response.data || []

    // Check if there are more transactions
    hasMore.value = transactions.value.length === filters.value.limit

  } catch (err) {
    console.error('Error loading transactions:', err)
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  loadingMore.value = true
  filters.value.skip += filters.value.limit

  try {
    const params = {
      limit: filters.value.limit,
      skip: filters.value.skip
    }

    if (filters.value.type) {
      params.type = filters.value.type
    }

    if (filters.value.start_date) {
      params.start_date = new Date(filters.value.start_date).toISOString()
    }

    if (filters.value.end_date) {
      params.end_date = new Date(filters.value.end_date).toISOString()
    }

    const response = await transactionAPI.getTransactions(params)
    const newTransactions = response.data || []

    transactions.value = [...transactions.value, ...newTransactions]
    hasMore.value = newTransactions.length === filters.value.limit

  } catch (err) {
    console.error('Error loading more transactions:', err)
  } finally {
    loadingMore.value = false
  }
}

const goToDetail = (transaction) => {
  router.push(`/transaction/${transaction.id}`)
}
</script>

<style scoped>
.history {
  padding-bottom: 80px;
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.filters-section {
  margin-bottom: var(--spacing-lg);
}

.filter-tabs {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: var(--spacing-xs);
}

.filter-tab {
  flex-shrink: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--tg-theme-hint-color);
  border-radius: var(--radius-lg);
  background-color: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-tab.active {
  border-color: var(--tg-theme-button-color);
  background-color: var(--tg-theme-button-color);
  color: white;
}

.date-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.date-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  border: 1px solid var(--tg-theme-hint-color);
  border-radius: var(--radius-md);
  background-color: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.date-btn.active {
  border-color: var(--tg-theme-button-color);
  background-color: rgba(42, 171, 238, 0.1);
  color: var(--tg-theme-button-color);
}

.custom-date-range {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.custom-date-range input {
  flex: 1;
  font-size: 14px;
}

.loading-container {
  display: flex;
  justify-content: center;
  padding: var(--spacing-xl) 0;
}

.transactions-container {
  animation: fadeIn 0.3s ease;
}

.transactions-summary {
  font-size: 13px;
  color: var(--tg-theme-hint-color);
  margin-bottom: var(--spacing-md);
  font-weight: 500;
}

.transactions-list {
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  text-align: center;
  min-height: 40vh;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}
</style>
