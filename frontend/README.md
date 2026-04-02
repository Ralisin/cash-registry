# 🎨 Frontend - Vue 3

Interfaccia utente della Finance App (Telegram Web App).

## 🚀 Setup Locale

### 1. Installa dipendenze

```bash
cd frontend
npm install
```

### 2. Configura variabili d'ambiente

```bash
# Copia .env.example in .env
cp .env.example .env

# Modifica .env con l'URL del tuo backend
```

### 3. Avvia dev server

```bash
npm run dev
```

L'app sarà disponibile su http://localhost:5173

## 🏗️ Build per produzione

```bash
npm run build
```

I file compilati saranno in `dist/`

## 📁 Struttura

```
frontend/
├── src/
│   ├── main.js              # Entry point
│   ├── App.vue              # Root component
│   ├── router/              # Vue Router
│   │   └── index.js
│   ├── views/               # Page components
│   │   ├── Dashboard.vue
│   │   ├── AddTransaction.vue
│   │   ├── History.vue
│   │   ├── Analytics.vue
│   │   └── Settings.vue
│   ├── components/          # Reusable components
│   │   ├── layout/
│   │   ├── transaction/
│   │   └── common/
│   ├── composables/         # Vue composables
│   │   ├── useTelegram.js
│   │   ├── useTheme.js
│   │   └── useBalance.js
│   ├── services/            # API services
│   │   └── api.js
│   ├── stores/              # Pinia stores
│   │   ├── user.js
│   │   └── transactions.js
│   ├── i18n/                # Translations
│   │   ├── index.js
│   │   ├── it.json
│   │   └── en.json
│   └── assets/              # Static assets
│       └── styles/
├── public/                  # Public files
├── index.html
├── vite.config.js
├── package.json
└── README.md
```

## 🎨 Design System

L'interfaccia segue il design di Telegram:

**Colori:**
- Primary: `#2AABEE` (blu Telegram)
- Background Light: `#FFFFFF`
- Background Dark: `#212121`
- Text Light: `#000000`
- Text Dark: `#FFFFFF`
- Secondary Text: `#707579`

**Typography:**
- Font: System font stack (San Francisco su iOS, Roboto su Android)

**Components:**
- Seguono le linee guida di Telegram Web App
- Mobile-first e touch-friendly
- Transizioni fluide

## 🌍 Internazionalizzazione

L'app supporta:
- 🇮🇹 Italiano
- 🇬🇧 Inglese

Le traduzioni sono in `src/i18n/`

## 🔌 Telegram Web App SDK

L'app utilizza il Telegram Web App SDK per:
- Autenticazione utente (initData)
- Tema (light/dark)
- BackButton
- MainButton
- HapticFeedback

Documentazione: https://core.telegram.org/bots/webapps

## 🚀 Deploy su Vercel

1. Crea account su https://vercel.com/
2. Import repository
3. Configura:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Aggiungi environment variable `VITE_API_BASE_URL`
5. Deploy!

## 📝 Note

- L'app è ottimizzata per mobile (Telegram Web App)
- Supporta dark mode automatico basato su Telegram theme
- Usa Telegram Web App SDK per integrazione nativa
