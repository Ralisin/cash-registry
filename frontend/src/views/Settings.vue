<template>
  <div class="page settings">
    <div class="container">
      <h1>{{ $t('settings.title') }}</h1>

      <!-- Profile Section -->
      <div class="section">
        <h2 class="section-title">{{ $t('settings.profile') }}</h2>
        <div class="settings-card">
          <div class="setting-item">
            <span class="setting-icon">👤</span>
            <div class="setting-info">
              <div class="setting-label">Nome</div>
              <div class="setting-value">{{ userStore.userName }}</div>
            </div>
          </div>
          <div class="setting-item">
            <span class="setting-icon">🆔</span>
            <div class="setting-info">
              <div class="setting-label">Telegram ID</div>
              <div class="setting-value">{{ userStore.telegramId }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Preferences Section -->
      <div class="section">
        <h2 class="section-title">{{ $t('settings.preferences') }}</h2>
        <div class="settings-card">
          <!-- Currency -->
          <div class="setting-item">
            <span class="setting-icon">💱</span>
            <div class="setting-info">
              <label class="setting-label" for="currency">{{ $t('settings.currency') }}</label>
              <select
                id="currency"
                v-model="form.currency"
                class="setting-select"
                @change="handleCurrencyChange"
              >
                <option value="EUR">EUR (€)</option>
                <option value="USD">USD ($)</option>
                <option value="GBP">GBP (£)</option>
                <option value="CHF">CHF</option>
              </select>
            </div>
          </div>

          <!-- Language -->
          <div class="setting-item">
            <span class="setting-icon">🌍</span>
            <div class="setting-info">
              <label class="setting-label" for="language">{{ $t('settings.language') }}</label>
              <select
                id="language"
                v-model="form.language"
                class="setting-select"
                @change="handleLanguageChange"
              >
                <option value="it">Italiano</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>

          <!-- Dark Mode -->
          <div class="setting-item">
            <span class="setting-icon">🌙</span>
            <div class="setting-info">
              <div class="setting-label">{{ $t('settings.darkMode') }}</div>
              <div class="setting-value text-muted">{{ darkModeStatus }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Balance Management -->
      <div class="section">
        <h2 class="section-title">{{ $t('settings.initialBalance') }}</h2>
        <div class="settings-card">
          <div class="balance-info">
            <div class="balance-row">
              <span>💵 {{ $t('dashboard.cash') }}</span>
              <span class="balance-amount">{{ formatAmount(userStore.balance?.initial_cash || 0) }}</span>
            </div>
            <div class="balance-row">
              <span>💳 {{ $t('dashboard.card') }}</span>
              <span class="balance-amount">{{ formatAmount(userStore.balance?.initial_card || 0) }}</span>
            </div>
            <div class="balance-row total">
              <span>💰 {{ $t('dashboard.totalBalance') }}</span>
              <span class="balance-amount">{{ formatAmount(userStore.balance?.initial_total || 0) }}</span>
            </div>
          </div>
          <button class="btn btn-secondary btn-block mt-md" @click="goToEditBalance">
            {{ $t('settings.editBalance') }}
          </button>
        </div>
      </div>

      <!-- Quick Links -->
      <div class="section">
        <div class="settings-card">
          <button class="setting-link" @click="goToCategories">
            <span class="setting-icon">🏷️</span>
            <span>{{ $t('settings.categories') }}</span>
            <span class="arrow">→</span>
          </button>
          <button class="setting-link" @click="goToExport">
            <span class="setting-icon">📤</span>
            <span>{{ $t('settings.export') }}</span>
            <span class="arrow">→</span>
          </button>
        </div>
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
import { useUserStore } from '../stores/user'
import { useTelegram } from '../composables/useTelegram'
import BottomNav from '../components/layout/BottomNav.vue'

const router = useRouter()
const userStore = useUserStore()
const { locale, t } = useI18n()
const { colorScheme, hapticFeedback } = useTelegram()

const form = ref({
  currency: 'EUR',
  language: 'it'
})

onMounted(() => {
  form.value.currency = userStore.currency
  form.value.language = userStore.language
  locale.value = userStore.language
})

const darkModeStatus = computed(() => {
  return colorScheme.value === 'dark' ? 'Attiva' : 'Disattivata'
})

const formatAmount = (amount) => {
  const currency = userStore.currency
  const symbols = {
    EUR: '€',
    USD: '$',
    GBP: '£',
    CHF: 'CHF'
  }

  const symbol = symbols[currency] || currency
  const formatted = amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

  return currency === 'EUR' ? `${formatted} ${symbol}` : `${symbol} ${formatted}`
}

const handleCurrencyChange = async () => {
  try {
    await userStore.updateSettings({ currency: form.value.currency })
    hapticFeedback('impact', 'light')
  } catch (err) {
    console.error('Error updating currency:', err)
  }
}

const handleLanguageChange = async () => {
  try {
    await userStore.updateSettings({ language: form.value.language })
    locale.value = form.value.language
    hapticFeedback('impact', 'light')
  } catch (err) {
    console.error('Error updating language:', err)
  }
}

const goToEditBalance = () => {
  // TODO: Implement edit balance modal or page
  alert('Feature coming soon')
}

const goToCategories = () => {
  router.push('/categories')
}

const goToExport = () => {
  // TODO: Implement export functionality
  alert('Feature coming soon')
}
</script>

<style scoped>
.settings {
  padding-bottom: 80px;
}

.container {
  padding: var(--spacing-lg) var(--spacing-md);
}

.section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--tg-theme-hint-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--spacing-sm);
}

.settings-card {
  background-color: var(--tg-theme-secondary-bg-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-sm);
  overflow: hidden;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.setting-info {
  flex: 1;
}

.setting-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.setting-value {
  font-size: 15px;
  color: var(--tg-theme-hint-color);
}

.setting-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--tg-theme-hint-color);
  border-radius: var(--radius-md);
  background-color: var(--tg-theme-bg-color);
  color: var(--tg-theme-text-color);
  font-size: 15px;
}

.balance-info {
  padding: var(--spacing-md);
}

.balance-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
}

.balance-row.total {
  border-top: 2px solid var(--tg-theme-hint-color);
  margin-top: var(--spacing-sm);
  padding-top: var(--spacing-md);
  font-weight: 600;
}

.balance-amount {
  font-weight: 600;
}

.setting-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  width: 100%;
  padding: var(--spacing-md);
  border: none;
  background: none;
  color: var(--tg-theme-text-color);
  font-size: 16px;
  cursor: pointer;
  transition: background-color var(--transition-fast);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.setting-link:last-child {
  border-bottom: none;
}

.setting-link:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.setting-link:active {
  background-color: rgba(0, 0, 0, 0.05);
}

.arrow {
  margin-left: auto;
  color: var(--tg-theme-hint-color);
}
</style>
