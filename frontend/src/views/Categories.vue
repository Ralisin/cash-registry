<template>
  <div class="page categories">
    <div class="container">
      <h1>{{ $t('categories.title') }}</h1>

      <!-- Add Button -->
      <button class="btn btn-primary btn-block mb-lg" @click="showAddModal = true">
        ➕ {{ $t('categories.add') }}
      </button>

      <!-- Default Categories -->
      <div class="section">
        <h2 class="section-title">{{ $t('categories.default') }}</h2>
        <div class="categories-list">
          <div
            v-for="category in defaultCategories"
            :key="category.id"
            class="category-item default"
          >
            <span class="category-icon">{{ category.icon || '📁' }}</span>
            <span class="category-name">{{ category.name }}</span>
            <span class="category-badge">Default</span>
          </div>
        </div>
      </div>

      <!-- Custom Categories -->
      <div class="section">
        <h2 class="section-title">{{ $t('categories.custom') }}</h2>
        <div v-if="customCategories.length === 0" class="empty-state">
          <p class="text-muted">Nessuna categoria personalizzata</p>
        </div>
        <div v-else class="categories-list">
          <div
            v-for="category in customCategories"
            :key="category.id"
            class="category-item custom"
          >
            <span class="category-icon">{{ category.icon || '📁' }}</span>
            <span class="category-name">{{ category.name }}</span>
            <button class="category-delete-btn" @click="handleDelete(category)">
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- Add Category Modal -->
      <div v-if="showAddModal" class="modal" @click.self="showAddModal = false">
        <div class="modal-content">
          <h2>{{ $t('categories.add') }}</h2>
          <form @submit.prevent="handleAdd">
            <div class="form-group">
              <label class="form-label">{{ $t('categories.name') }} *</label>
              <input
                v-model="newCategory.name"
                type="text"
                class="form-input"
                required
                maxlength="50"
              />
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('categories.icon') }}</label>
              <input
                v-model="newCategory.icon"
                type="text"
                class="form-input"
                placeholder="Es: 🏕️"
                maxlength="10"
              />
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="showAddModal = false">
                {{ $t('common.cancel') }}
              </button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? $t('common.loading') : $t('common.save') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCategoriesStore } from '../stores/categories'
import { useTelegram } from '../composables/useTelegram'
import BottomNav from '../components/layout/BottomNav.vue'

const categoriesStore = useCategoriesStore()
const { hapticFeedback, showConfirm, showAlert } = useTelegram()

const loading = ref(false)
const showAddModal = ref(false)
const newCategory = ref({
  name: '',
  icon: ''
})

onMounted(async () => {
  if (categoriesStore.categories.length === 0) {
    await categoriesStore.fetchCategories()
  }
})

const defaultCategories = computed(() => {
  return categoriesStore.categories.filter(c => c.is_default)
})

const customCategories = computed(() => {
  return categoriesStore.categories.filter(c => !c.is_default)
})

const handleAdd = async () => {
  loading.value = true

  try {
    await categoriesStore.createCategory({
      name: newCategory.value.name,
      icon: newCategory.value.icon || null
    })

    hapticFeedback('notification', 'success')
    await showAlert('✅ Categoria creata')

    // Reset form
    newCategory.value = { name: '', icon: '' }
    showAddModal.value = false

  } catch (err) {
    console.error('Error creating category:', err)
    hapticFeedback('notification', 'error')
    await showAlert('❌ Errore durante la creazione')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (category) => {
  hapticFeedback('impact', 'medium')

  const confirmed = await showConfirm(
    `Eliminare la categoria "${category.name}"?\n\nSe è usata in transazioni, dovrai selezionare una categoria sostitutiva.`
  )

  if (!confirmed) return

  loading.value = true

  try {
    // For simplicity, use first default category as replacement
    const replacementId = defaultCategories.value[0]?.id || null

    await categoriesStore.deleteCategory(category.id, replacementId)

    hapticFeedback('notification', 'success')
    await showAlert('✅ Categoria eliminata')

  } catch (err) {
    console.error('Error deleting category:', err)
    hapticFeedback('notification', 'error')
    await showAlert('❌ Errore durante l\'eliminazione')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.categories {
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
  margin-bottom: var(--spacing-md);
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--tg-theme-secondary-bg-color);
  border-radius: var(--radius-md);
  transition: transform var(--transition-fast);
}

.category-item:active {
  transform: scale(0.98);
}

.category-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.category-name {
  flex: 1;
  font-size: 16px;
  font-weight: 500;
}

.category-badge {
  font-size: 11px;
  padding: 4px 8px;
  background-color: rgba(42, 171, 238, 0.1);
  color: var(--tg-theme-button-color);
  border-radius: var(--radius-sm);
  font-weight: 600;
  text-transform: uppercase;
}

.category-delete-btn {
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  opacity: 0.6;
  transition: opacity var(--transition-fast);
}

.category-delete-btn:hover {
  opacity: 1;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl);
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-md);
}

.modal-content {
  background-color: var(--tg-theme-bg-color);
  border-radius: var(--radius-xl);
  padding: var(--spacing-lg);
  width: 100%;
  max-width: 400px;
  box-shadow: var(--shadow-lg);
}

.modal-content h2 {
  margin-bottom: var(--spacing-lg);
}

.modal-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.modal-actions button {
  flex: 1;
}
</style>
