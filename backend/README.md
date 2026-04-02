# 🔧 Backend - FastAPI + MongoDB

Backend API per la gestione finanziaria scout.

## 🚀 Setup Locale

### 1. Crea ambiente virtuale

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Installa dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura variabili d'ambiente

```bash
# Copia .env.example in .env
cp .env.example .env

# Modifica .env con i tuoi valori
```

#### Come ottenere le credenziali:

**MongoDB Atlas:**
1. Vai su https://cloud.mongodb.com/
2. Crea un account gratuito
3. Crea un cluster (M0 Free tier)
4. Database Access → Add Database User
5. Network Access → Add IP Address (0.0.0.0/0 per development)
6. Clusters → Connect → Connect your application → Copia connection string

**Telegram Bot Token:**
1. Apri Telegram e cerca @BotFather
2. Invia `/newbot`
3. Segui le istruzioni
4. Copia il token ricevuto

### 4. Avvia il server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production (Render)
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

## 📡 API Endpoints

Una volta avviato, la documentazione interattiva è disponibile a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints principali:

**Users:**
- `POST /users` - Registra nuovo utente
- `GET /users/{telegram_id}` - Ottieni utente
- `PATCH /users/{telegram_id}/settings` - Aggiorna impostazioni

**Balance:**
- `GET /balance/{telegram_id}` - Ottieni saldo
- `POST /balance/initialize` - Imposta saldo iniziale
- `PATCH /balance/update` - Modifica saldo

**Transactions:**
- `POST /transactions` - Crea transazione
- `GET /transactions` - Lista transazioni (con filtri)
- `GET /transactions/{id}` - Dettaglio transazione
- `PATCH /transactions/{id}` - Modifica transazione
- `DELETE /transactions/{id}` - Elimina transazione
- `POST /transactions/transfer` - Trasferimento

**Categories:**
- `GET /categories/{telegram_id}` - Lista categorie
- `POST /categories` - Crea categoria custom
- `PATCH /categories/{id}` - Modifica categoria
- `DELETE /categories/{id}` - Elimina categoria

**Export:**
- `GET /export/csv` - Export CSV
- `GET /export/excel` - Export Excel
- `GET /export/pdf` - Export PDF

## 📁 Struttura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point FastAPI
│   ├── config.py            # Configurazione
│   ├── database.py          # Setup MongoDB
│   ├── models/              # Modelli Beanie
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── category.py
│   │   └── transaction.py
│   ├── routes/              # API routes
│   │   ├── users.py
│   │   ├── transactions.py
│   │   ├── categories.py
│   │   └── export.py
│   └── utils/               # Utility functions
│       ├── telegram_auth.py
│       └── validators.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🧪 Testing

```bash
# TODO: Add tests
pytest
```

## 🚀 Deploy su Render

1. Crea account su https://render.com/
2. New → Web Service
3. Connect repository
4. Configura:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Aggiungi environment variables da .env
6. Deploy!

## 📝 Note

- Il server usa la porta 10000 per Render (requisito free tier)
- CORS configurato per accettare richieste dal frontend
- Telegram initData viene validato per autenticazione
