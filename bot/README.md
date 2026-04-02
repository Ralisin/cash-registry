# 🤖 Telegram Bot

Bot Telegram per l'accesso alla Finance App.

## 🚀 Setup Locale

### 1. Installa dipendenze

```bash
cd bot
pip install -r requirements.txt
```

### 2. Configura variabili d'ambiente

```bash
# Copia .env.example in .env
cp .env.example .env

# Modifica .env con i tuoi valori
```

#### Come ottenere il Bot Token:

1. Apri Telegram e cerca **@BotFather**
2. Invia `/newbot`
3. Scegli un nome per il bot (es. "Scout Finance Bot")
4. Scegli un username (deve finire con "bot", es. "scout_finance_bot")
5. Copia il token ricevuto
6. Incollalo in `.env` come `TELEGRAM_BOT_TOKEN`

### 3. Configura Web App

Dopo aver ottenuto il token, devi configurare la Web App:

1. Invia a @BotFather: `/mybots`
2. Seleziona il tuo bot
3. Bot Settings → Menu Button → Configure Menu Button
4. Invia l'URL della tua web app (es. https://your-app.vercel.app)

### 4. Avvia il bot

```bash
python bot.py
```

## 🎯 Comandi Bot

- `/start` - Registra utente e mostra pulsante per aprire l'app
- `/app` - Apri la Web App

## 📁 Struttura

```
bot/
├── bot.py              # Main bot logic
├── requirements.txt    # Dipendenze
├── .env.example        # Template variabili
└── README.md          # Questo file
```

## 🚀 Deploy

Il bot può girare su Render insieme al backend o su un servizio separato.

### Opzione 1: Webhook (Produzione su Render)

```python
# In bot.py, usa webhook invece di polling
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv("PORT", 10000)),
    url_path=TELEGRAM_BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}"
)
```

### Opzione 2: Polling (Development)

```python
# Default, usato in development
application.run_polling()
```

## 📝 Note

- Il bot comunica con il backend per registrare gli utenti
- La Web App si apre tramite pulsante inline
- L'autenticazione avviene tramite Telegram Web App initData
