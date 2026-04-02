# 📊 Telegram Finance App - Scout Agesci

Sistema completo di gestione finanziaria per la cassa di reparto scout, integrato con Telegram.

## 🎯 Features

- 💰 Gestione saldi (contanti e conto)
- 📝 Tracciamento spese ed entrate
- 🔄 Trasferimenti tra conti
- 📊 Analytics e statistiche
- 📤 Export dati (CSV, Excel, PDF)
- 🏷️ Categorie personalizzabili
- 🌍 Multi-lingua (IT/EN)
- 🌙 Dark mode
- 📱 Mobile-first (Telegram Web App)

## 🧱 Tech Stack

- **Backend:** FastAPI + MongoDB (Beanie ODM)
- **Frontend:** Vue 3 (Composition API) + Vite
- **Bot:** python-telegram-bot
- **Hosting:** Render + Vercel + MongoDB Atlas (Free tier)

## 📁 Project Structure

```
cash-registry/
├── backend/          # FastAPI backend
├── bot/              # Telegram bot
├── frontend/         # Vue 3 frontend
└── docs/             # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account
- Telegram Bot Token

### Local Development

Vedi le istruzioni specifiche in:
- [Backend README](./backend/README.md)
- [Bot README](./bot/README.md)
- [Frontend README](./frontend/README.md)

## 📝 Environment Variables

Ogni componente richiede le proprie variabili d'ambiente. Consulta i file `.env.example` in:
- `backend/.env.example`
- `bot/.env.example`
- `frontend/.env.example`

## 🌐 Deployment

- **Backend:** Deploy su Render
- **Frontend:** Deploy su Vercel
- **Database:** MongoDB Atlas
- **Bot:** Webhook su Render

Guida dettagliata al deployment: [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📖 Documentation

- [Specifiche Progetto](./CLAUDE.md)
- [Piano Sprint](./SPRINT_PLAN.md)
- [API Documentation](./backend/API.md)

## 📄 License

MIT License - vedi [LICENSE](./LICENSE)
