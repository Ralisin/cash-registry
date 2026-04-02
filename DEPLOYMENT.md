# 🚀 Deployment Guide

Guida completa per il deploy dell'app su servizi gratuiti.

## 📋 Prerequisiti

Prima di iniziare, avrai bisogno di:

1. Account GitHub (per repository)
2. Account MongoDB Atlas (database)
3. Account Render (backend + bot)
4. Account Vercel (frontend)
5. Telegram Bot Token (da @BotFather)

---

## 1️⃣ MongoDB Atlas Setup

### Crea Database

1. Vai su https://cloud.mongodb.com/
2. Crea un account gratuito
3. **Create a New Cluster**
   - Scegli **M0 Free tier**
   - Region: Scegli la più vicina (es. Frankfurt per EU)
   - Cluster Name: `scout-finance`

### Configura Accesso

4. **Database Access** (menu laterale)
   - Add New Database User
   - Username: `scout_admin` (o a tua scelta)
   - Password: Genera una password sicura (salvala!)
   - Database User Privileges: `Read and write to any database`

5. **Network Access**
   - Add IP Address
   - **Allow Access from Anywhere**: `0.0.0.0/0`
   - (Necessario per Render/Vercel)

### Ottieni Connection String

6. **Clusters** → **Connect**
   - Connect your application
   - Driver: Python, Version: 3.11 or later
   - Copia la connection string:
   ```
   mongodb+srv://scout_admin:<password>@scout-finance.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - Sostituisci `<password>` con la password del database user
   - Aggiungi il nome del database: `scout-finance.xxxxx.mongodb.net/scout_finance`

---

## 2️⃣ Telegram Bot Setup

### Crea Bot

1. Apri Telegram e cerca **@BotFather**
2. Invia `/newbot`
3. Nome bot: `Scout Finance Bot` (o a tua scelta)
4. Username: `scout_finance_bot` (deve finire con `_bot`)
5. **Salva il token** ricevuto (es. `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Configura Menu Button (dopo deploy frontend)

Dopo aver deployato il frontend su Vercel:

1. Invia a @BotFather: `/mybots`
2. Seleziona il tuo bot
3. **Bot Settings** → **Menu Button**
4. **Configure Menu Button**
5. URL: `https://your-app.vercel.app` (URL Vercel)
6. Text: `Apri App` o `Open App`

---

## 3️⃣ Backend Deploy (Render)

### Setup Repository

1. Assicurati che il progetto sia su GitHub
2. Commit e push di tutto il codice

### Crea Web Service

1. Vai su https://render.com/
2. Crea account (puoi usare GitHub)
3. **New** → **Web Service**
4. **Connect repository** → Seleziona il tuo repo
5. Configurazione:
   - **Name:** `scout-finance-api`
   - **Region:** Frankfurt (o più vicino)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - **Instance Type:** Free

### Aggiungi Environment Variables

Nella sezione **Environment**:

```
MONGODB_URL=mongodb+srv://scout_admin:password@scout-finance.xxxxx.mongodb.net/scout_finance
DATABASE_NAME=scout_finance
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
API_HOST=0.0.0.0
API_PORT=10000
DEBUG=false
FRONTEND_URL=https://your-app.vercel.app
SECRET_KEY=[genera con: openssl rand -hex 32]
```

### Deploy

6. **Create Web Service**
7. Attendi il deploy (5-10 minuti)
8. **Salva l'URL** (es. `https://scout-finance-api.onrender.com`)

⚠️ **Nota:** Il free tier di Render va in sleep dopo 15 min di inattività. Il primo accesso dopo sleep può richiedere 30-60 secondi.

---

## 4️⃣ Frontend Deploy (Vercel)

### Setup Vercel

1. Vai su https://vercel.com/
2. Crea account (puoi usare GitHub)
3. **Add New** → **Project**
4. **Import Git Repository** → Seleziona il tuo repo

### Configurazione Build

5. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### Aggiungi Environment Variable

6. **Environment Variables:**
   ```
   VITE_API_BASE_URL=https://scout-finance-api.onrender.com
   VITE_APP_NAME=Scout Finance
   ```

### Deploy

7. **Deploy**
8. Attendi il deploy (2-3 minuti)
9. **Salva l'URL** (es. `https://scout-finance.vercel.app`)

### Configura Domain (opzionale)

- Settings → Domains → Aggiungi un dominio custom

---

## 5️⃣ Bot Deploy (Render)

### Opzione A: Deploy separato (raccomandato)

1. **New** → **Web Service** (come per il backend)
2. Configurazione:
   - **Name:** `scout-finance-bot`
   - **Root Directory:** `bot`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

3. Environment Variables:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   BACKEND_API_URL=https://scout-finance-api.onrender.com
   WEB_APP_URL=https://scout-finance.vercel.app
   WEBHOOK_URL=https://scout-finance-bot.onrender.com
   ```

### Opzione B: Insieme al Backend

Aggiungi il bot nel backend e modifica lo start command:

```bash
# Crea uno script start.sh
python bot/bot.py & uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

## 6️⃣ Verifica Deploy

### Test Backend

```bash
curl https://scout-finance-api.onrender.com/docs
```

Dovresti vedere la documentazione Swagger.

### Test Frontend

Apri `https://scout-finance.vercel.app` in un browser. Dovresti vedere l'app.

### Test Bot

1. Apri Telegram
2. Cerca il tuo bot (es. `@scout_finance_bot`)
3. Invia `/start`
4. Clicca sul pulsante per aprire l'app
5. Verifica che l'app si apra correttamente

### Test Completo

1. Registrati tramite bot
2. Imposta saldi iniziali
3. Aggiungi una transazione
4. Verifica che appaia nella dashboard
5. Controlla che i saldi si aggiornino

---

## 🔄 Update & Redeploy

### Backend/Bot

Render fa auto-deploy su ogni push a GitHub. Oppure:
- Dashboard Render → Service → **Manual Deploy** → **Deploy latest commit**

### Frontend

Vercel fa auto-deploy su ogni push. Oppure:
- Dashboard Vercel → Project → **Deployments** → **Redeploy**

---

## 🐛 Troubleshooting

### Backend non risponde

- Verifica log su Render: Dashboard → Service → **Logs**
- Controlla le environment variables
- Verifica la connection string MongoDB

### Frontend non si connette al backend

- Verifica `VITE_API_BASE_URL` su Vercel
- Controlla CORS nel backend
- Verifica che il backend sia online (Render free tier dorme)

### Bot non risponde

- Verifica il token su @BotFather con `/mybots`
- Controlla i log del bot su Render
- Verifica che `WEB_APP_URL` sia corretto

### Telegram Web App non si apre

- Verifica Menu Button su @BotFather
- Controlla che l'URL Vercel sia corretto
- Verifica che il frontend sia online

### Database non si connette

- Verifica IP whitelist su MongoDB Atlas (deve essere 0.0.0.0/0)
- Controlla username/password nella connection string
- Verifica che il cluster sia attivo

---

## 📊 Monitoring

### Render

- Dashboard → Service → **Metrics**
- Visualizza CPU, Memory, Requests

### Vercel

- Dashboard → Project → **Analytics**
- Visualizza visite, performance

### MongoDB Atlas

- Dashboard → Cluster → **Metrics**
- Visualizza operazioni, storage

---

## 💰 Costi

**Tutto gratuito!**

- MongoDB Atlas M0: Free (512 MB storage)
- Render Free Tier: 750h/mese (suffizienti per 1 servizio 24/7)
- Vercel Hobby: Gratis (100 GB bandwidth/mese)
- Telegram Bot: Gratis

**Limiti:**
- Render: Sleep dopo 15 min inattività
- MongoDB: Max 512 MB storage
- Vercel: Max 100 GB bandwidth/mese

---

## ✅ Checklist Deploy

- [ ] MongoDB Atlas cluster creato
- [ ] Database user configurato
- [ ] Connection string salvata
- [ ] Telegram Bot creato
- [ ] Bot token salvato
- [ ] Backend deployato su Render
- [ ] Frontend deployato su Vercel
- [ ] Bot deployato
- [ ] Menu Button configurato
- [ ] Test end-to-end completato
- [ ] URL documentati

---

## 📝 Note Finali

- **Backup:** MongoDB Atlas fa backup automatici
- **SSL/HTTPS:** Render e Vercel forniscono HTTPS automaticamente
- **Logs:** Consulta sempre i log per debugging
- **Updates:** Puoi fare redeploy in qualsiasi momento

Buon deploy! 🚀
