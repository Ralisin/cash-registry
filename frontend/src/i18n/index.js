/**
 * i18n Configuration
 * Internationalization setup for Italian and English
 */

import { createI18n } from 'vue-i18n'
import it from './it.json'
import en from './en.json'

const i18n = createI18n({
  legacy: false,
  locale: 'it', // default locale
  fallbackLocale: 'en',
  messages: {
    it,
    en
  }
})

export default i18n
