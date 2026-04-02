/**
 * Vue Router Configuration
 * Defines app routes and navigation
 */

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { title: 'Dashboard' }
    },
    {
      path: '/setup',
      name: 'setup',
      component: () => import('../views/InitialSetup.vue'),
      meta: { title: 'Setup Iniziale' }
    },
    {
      path: '/add-transaction',
      name: 'add-transaction',
      component: () => import('../views/AddTransaction.vue'),
      meta: { title: 'Nuova Transazione' }
    },
    {
      path: '/transfer',
      name: 'transfer',
      component: () => import('../views/Transfer.vue'),
      meta: { title: 'Trasferimento' }
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/History.vue'),
      meta: { title: 'Storico' }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/Analytics.vue'),
      meta: { title: 'Statistiche' }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/Settings.vue'),
      meta: { title: 'Impostazioni' }
    },
    {
      path: '/transaction/:id',
      name: 'transaction-detail',
      component: () => import('../views/TransactionDetail.vue'),
      meta: { title: 'Dettaglio Transazione' }
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/Categories.vue'),
      meta: { title: 'Categorie' }
    }
  ]
})

// Navigation guard to update Telegram back button
router.beforeEach((to, from, next) => {
  // Update page title
  document.title = to.meta.title ? `${to.meta.title} - Scout Finance` : 'Scout Finance'

  // Handle Telegram back button
  if (window.Telegram?.WebApp) {
    if (to.name !== 'dashboard' && to.name !== 'setup') {
      window.Telegram.WebApp.BackButton.show()
    } else {
      window.Telegram.WebApp.BackButton.hide()
    }
  }

  next()
})

// Handle Telegram back button click
if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.BackButton.onClick(() => {
    router.back()
  })
}

export default router
