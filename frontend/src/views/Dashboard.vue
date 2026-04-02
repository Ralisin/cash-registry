<template>
  <div class="page dashboard">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p class="text-muted mt-md">{{ $t('common.loading') }}</p>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Header -->
        <div class="dashboard-header">
          <h1>{{ $t('dashboard.title') }}</h1>
          <p class="welcome-text">👋 {{ userStore.userName }}</p>
        </div>

        <!-- Balance Cards -->
        <div class="balance-grid">
          <BalanceCard
            :title="$t('dashboard.totalBalance')"
            :amount="userStore.totalBalance"
            icon="💰"
            variant="primary"
          />
          <BalanceCard
            :title="$t('dashboard.cash')"
            :amount="userStore.cashBalance"
            icon="💵"
            variant="default"
          />
          <BalanceCard
            :title="$t('dashboard.card')"
            :amount="userStore.cardBalance"
            icon="💳"
            variant="default"
          />
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions">
          <button class="action-btn primary" @click="goToAddTransaction">
            <span class="btn-icon">➕</span>
            <span>{{ $t('dashboard.addTransaction') }}</span>
          </button>
          <button class="action-btn secondary" @click="goToTransfer">
            <span class="btn-icon">🔄</span>
            <span>{{ $t('dashboard.transfer') }}</span>
          </button>
        </div>

        <!-- Recent Transactions -->
        <div class="section">
          <div class="section-header">
            <h2>{{ $t('dashboard.recentTransactions') }}</h2>
            <router-link to="/history" class="section-link">
              {{ $t('history.title') }} →
            </router-link>
          </div>

          <div v-if="recentTransactions.length === 0" class="empty-state">
            <span class="empty-icon">📝</span>
            <p>{{ $t('dashboard.noTransactions') }}</p>
            <button class="btn btn-primary mt-md" @click="goToAddTransaction">
              {{ $t('dashboard.addTransaction') }}
            </button>
          </div>

          <div v-else class="transactions-list">
            <TransactionItem
              v-for="transaction in recentTransactions"
              :key="transaction.id"
              :transaction="transaction"
              @click="goToTransactionDetail"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { transactionAPI } from '../services/api'
import BalanceCard from '../components/common/BalanceCard.vue'
import TransactionItem from '../components/transaction/TransactionItem.vue'
import BottomNav from '../components/layout/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const recentTransactions = ref([])
const error = ref(null)

onMounted(async () => {
  await loadDashboard()
})

const loadDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    // Check if user needs setup
    if (userStore.totalBalance === 0 && !userStore.balance?.initial_total) {
      router.push('/setup')
      return
    }

    // Fetch recent transactions
    const response = await transactionAPI.getTransactions({ limit: 10 })
    recentTransactions.value = response.data || []

  } catch (err) {
    console.error('Error loading dashboard:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const goToAddTransaction = () => {
  router.push('/add-transaction')
}

const goToTransfer = () => {
  router.push('/transfer')
}

const goToTransactionDetail = (transaction) => {
  router.push(`/transaction/${transaction.id}`)
}
</script>

<style scoped>
.dashboard {
  padding-bottom: 80px;
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.dashboard-header {
  margin-bottom: var(--spacing-lg);
}

.dashboard-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-xs);
}

.welcome-text {
  color: var(--tg-theme-hint-color);
  font-size: 16px;
}

.balance-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg) var(--spacing-md);
  border: none;
  border-radius: var(--radius-lg);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  gap: var(--spacing-sm);
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn.primary {
  background: linear-gradient(135deg, #2AABEE 0%, #229ED9 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(42, 171, 238, 0.3);
}

.action-btn.secondary {
  background-color: var(--tg-theme-secondary-bg-color);
  color: var(--tg-theme-text-color);
}

.btn-icon {
  font-size: 32px;
}

.section {
  margin-bottom: var(--spacing-xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.section-header h2 {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.section-link {
  font-size: 14px;
  color: var(--tg-theme-button-color);
  text-decoration: none;
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-state p {
  color: var(--tg-theme-hint-color);
  margin-bottom: var(--spacing-md);
}

.transactions-list {
  display: flex;
  flex-direction: column;
}
</style>
