/**
 * API Service
 * Handles all HTTP requests to the backend API
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add Telegram initData
api.interceptors.request.use(
  (config) => {
    // Add Telegram initData to headers if available
    if (window.Telegram?.WebApp?.initData) {
      config.headers['X-Telegram-Init-Data'] = window.Telegram.WebApp.initData
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ===== USER ENDPOINTS =====

export const userAPI = {
  /**
   * Register/Get user
   */
  createUser: (initData) => {
    return api.post('/users/', { init_data: initData })
  },

  /**
   * Get user by telegram_id
   */
  getUser: (telegramId) => {
    return api.get(`/users/${telegramId}`)
  },

  /**
   * Update user settings
   */
  updateSettings: (telegramId, settings) => {
    return api.patch(`/users/${telegramId}/settings`, settings)
  },

  /**
   * Get balance
   */
  getBalance: (telegramId) => {
    return api.get(`/users/${telegramId}/balance`)
  },

  /**
   * Initialize balance
   */
  initializeBalance: (telegramId, data) => {
    return api.post(`/users/${telegramId}/balance/initialize`, data)
  },

  /**
   * Update balance
   */
  updateBalance: (telegramId, data) => {
    return api.patch(`/users/${telegramId}/balance`, data)
  }
}

// ===== TRANSACTION ENDPOINTS =====

export const transactionAPI = {
  /**
   * Create transaction
   */
  createTransaction: (data) => {
    return api.post('/transactions/', data)
  },

  /**
   * Create transfer
   */
  createTransfer: (data) => {
    return api.post('/transactions/transfer', data)
  },

  /**
   * Get transactions with filters
   */
  getTransactions: (params = {}) => {
    return api.get('/transactions/', { params })
  },

  /**
   * Get transaction by ID
   */
  getTransaction: (id) => {
    return api.get(`/transactions/${id}`)
  },

  /**
   * Update transaction
   */
  updateTransaction: (id, data) => {
    return api.patch(`/transactions/${id}`, data)
  },

  /**
   * Delete transaction
   */
  deleteTransaction: (id) => {
    return api.delete(`/transactions/${id}`)
  }
}

// ===== CATEGORY ENDPOINTS =====

export const categoryAPI = {
  /**
   * Get all categories (default + user custom)
   */
  getCategories: () => {
    return api.get('/categories/')
  },

  /**
   * Get category by ID
   */
  getCategory: (id) => {
    return api.get(`/categories/${id}`)
  },

  /**
   * Create custom category
   */
  createCategory: (data) => {
    return api.post('/categories/', data)
  },

  /**
   * Update category
   */
  updateCategory: (id, data) => {
    return api.patch(`/categories/${id}`, data)
  },

  /**
   * Delete category
   */
  deleteCategory: (id, replacementCategoryId = null) => {
    const params = replacementCategoryId ? { replacement_category_id: replacementCategoryId } : {}
    return api.delete(`/categories/${id}`, { params })
  }
}

// ===== EXPORT ENDPOINTS (to be implemented) =====

export const exportAPI = {
  /**
   * Export as CSV
   */
  exportCSV: (params = {}) => {
    return api.get('/export/csv', { params, responseType: 'blob' })
  },

  /**
   * Export as Excel
   */
  exportExcel: (params = {}) => {
    return api.get('/export/excel', { params, responseType: 'blob' })
  },

  /**
   * Export as PDF
   */
  exportPDF: (params = {}) => {
    return api.get('/export/pdf', { params, responseType: 'blob' })
  }
}

export default api
