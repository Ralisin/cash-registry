/**
 * Categories Store (Pinia)
 * Manages categories state
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoryAPI } from '../services/api'

export const useCategoriesStore = defineStore('categories', () => {
  // State
  const categories = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Actions
  async function fetchCategories() {
    loading.value = true
    error.value = null

    try {
      const response = await categoryAPI.getCategories()
      categories.value = response.data || []
      return categories.value
    } catch (err) {
      error.value = err.message
      console.error('Error fetching categories:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCategory(data) {
    loading.value = true
    error.value = null

    try {
      const response = await categoryAPI.createCategory(data)
      categories.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error creating category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCategory(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await categoryAPI.updateCategory(id, data)
      const index = categories.value.findIndex(c => c.id === id)
      if (index !== -1) {
        categories.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error updating category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCategory(id, replacementId = null) {
    loading.value = true
    error.value = null

    try {
      await categoryAPI.deleteCategory(id, replacementId)
      categories.value = categories.value.filter(c => c.id !== id)
    } catch (err) {
      error.value = err.message
      console.error('Error deleting category:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    categories,
    loading,
    error,
    // Actions
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory
  }
})
