# 🚀 Quick Start Guide - Scout Finance App

Guida rapida per far partire il progetto in locale.

---

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (free)
- Telegram Bot Token

---

## ⚡ Setup Rapido (5 minuti)

### 1. MongoDB Atlas (2 min)

1. Vai su https://cloud.mongodb.com/
2. Registrati gratis
3. Crea cluster M0 (free)
4. Database Access → Add User (username + password)
5. Network Access → Add IP → `0.0.0.0/0`
6. Clusters → Connect → Connection String
7. Copia: `mongodb+srv://username:password@cluster.mongodb.net/`

### 2. Telegram Bot (1 min)

1. Apri Telegram → cerca `@BotFather`
2. Invia `/newbot`
3. Nome: "Scout Finance Bot"
4. Username: "scout_finance_bot"
5. Copia il **token** ricevuto

### 3. Backend (1 min)

```bash
cd backend

# Crea .env
cp .env.example .env

# Modifica .env con i tuoi valori:
# - MONGODB_URL=<connection string MongoDB>
# - TELEGRAM_BOT_TOKEN=<token bot>
# - FRONTEND_URL=http://localhost:5173
# - SECRET_KEY=<genera con: openssl rand -hex 32>

# Installa dipendenze
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Avvia server
uvicorn app.main:app --reload --port 8000
```

✅ Backend running su http://localhost:8000
✅ Docs API su http://localhost:8000/docs

### 4. Bot (30 sec)

```bash
cd bot

# Crea .env
cp .env.example .env

# Modifica .env:
# - TELEGRAM_BOT_TOKEN=<token bot>
# - BACKEND_API_URL=http://localhost:8000
# - WEB_APP_URL=http://localhost:5173

# Installa e avvia
pip install -r requirements.txt
python bot.py
```

✅ Bot running in polling mode

### 5. Frontend (1 min)

```bash
cd frontend

# Crea .env
cp .env.example .env

# Modifica .env:
# - VITE_API_BASE_URL=http://localhost:8000

# Installa e avvia
npm install
npm run dev
```

✅ Frontend running su http://localhost:5173

---

## 🧪 Test Locale

### Opzione A: Browser Desktop (simulazione)

1. Apri http://localhost:5173
2. Nota: initData Telegram non sarà valido
3. Per testare: disabilita temporaneamente validation in backend

### Opzione B: Telegram Mobile (reale)

1. Pubblica frontend su Vercel temporaneo
2. @BotFather → Bot Settings → Menu Button → URL Vercel
3. Apri bot su Telegram → clicca pulsante
4. **Vero testing con initData valido!**

### Opzione C: ngrok (migliore per dev locale)

```bash
# Terminal 1: Backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
npm run dev

# Terminal 3: Expose frontend
ngrok http 5173

# Usa URL ngrok HTTPS per Bot Settings in @BotFather
```

---

## 📱 Primo Utilizzo

1. **Apri Telegram** → cerca il tuo bot
2. **`/start`** → Registrazione
3. **Clicca "Apri Finance App"**
4. **Setup iniziale:** Imposta saldi (es. Contanti: 500€, Conto: 1000€)
5. **Dashboard:** Vedi i tuoi saldi
6. **Aggiungi prima spesa:**
   - Tipo: Spesa
   - Importo: 50€
   - Categoria: Campo/Uscite
   - Conto: Contanti
   - Conferma
7. **Verifica:** Saldo contanti è ora 450€!

---

## 🐛 Troubleshooting

### Backend non si avvia

- ✅ Verifica MongoDB URL in `.env`
- ✅ Verifica bot token in `.env`
- ✅ `pip install -r requirements.txt` completato?

### Frontend errore API

- ✅ Backend running su porta 8000?
- ✅ `VITE_API_BASE_URL` in `.env` corretto?
- ✅ CORS configurato in backend?

### Bot non risponde

- ✅ Token corretto in `.env`?
- ✅ `python bot.py` running?
- ✅ Log errori nel terminal?

### Web App non si apre da Telegram

- ✅ Menu Button configurato in @BotFather?
- ✅ URL frontend accessibile (HTTPS per prod)?
- ✅ Frontend deployed o ngrok per local?

---

## 📚 Next Steps

1. ✅ Leggi `PROJECT_SUMMARY.md` per overview completo
2. ✅ Leggi `DEPLOYMENT.md` per deploy su Render + Vercel
3. ✅ Consulta `/docs` endpoint per API reference
4. ✅ Personalizza categorie scout in `backend/app/models/category.py`

---

## 🎯 Features Principali da Testare

- [ ] Registrazione utente via bot
- [ ] Setup saldi iniziali
- [ ] Add expense (verifica balance decrementa)
- [ ] Add income (verifica balance incrementa)
- [ ] Transfer cash→card (verifica entrambi)
- [ ] View transaction detail
- [ ] Delete transaction (verifica balance ripristinato)
- [ ] Filter history per tipo
- [ ] Filter history per Anno Scout (Settembre-Giugno)
- [ ] Add custom category
- [ ] Delete custom category
- [ ] Change currency
- [ ] Change language
- [ ] Dark mode (auto da Telegram)

---

## 💡 Tips

### Development

- **API Docs:** http://localhost:8000/docs (test endpoints)
- **Vue Devtools:** Installa per debug Pinia stores
- **MongoDB Compass:** GUI per vedere database
- **Postman:** Test API manualmente

### Testing Telegram Features

- **Haptic Feedback:** Solo su device fisico
- **Theme:** Testa light + dark in Telegram settings
- **BackButton:** Auto-gestito da Vue Router
- **initData:** Valido solo da vero Telegram Web App

### Performance

- **Backend:** ~100ms response time
- **Frontend:** First load ~1s, poi instant
- **MongoDB:** Free tier ottimo per migliaia di tx

---

## 🚀 Ready for Production?

Quando sei pronto per il deploy:

1. **Leggi `DEPLOYMENT.md`** (step-by-step completo)
2. **Setup Render** per backend
3. **Setup Vercel** per frontend
4. **Configura bot** con URL produzione
5. **Test completo** end-to-end

**Tempo totale deploy:** ~30 minuti

---

**Happy Coding! 🏕️**

Per supporto, consulta i README in ogni cartella o `PROJECT_SUMMARY.md` per dettagli completi.
