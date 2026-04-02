"""
Scout Finance Telegram Bot
Provides access to the Finance Web App through Telegram.
"""

import os
import logging
import httpx
from dotenv import load_dotenv

from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:5173")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Empty for polling mode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /start command.
    Registers the user and shows the Web App button.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"User {user.id} ({user.first_name}) started the bot")

    # Register user via backend API
    try:
        # Create a simple registration payload
        # Note: In a real scenario, we'd need initData, but for bot registration
        # we can use basic user info
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_API_URL}/users",
                json={
                    "telegram_id": user.id,
                    "name": f"{user.first_name} {user.last_name or ''}".strip(),
                    "username": user.username
                },
                timeout=10.0
            )

            if response.status_code in [200, 201]:
                logger.info(f"User {user.id} registered successfully")
            else:
                logger.warning(f"Failed to register user {user.id}: {response.text}")

    except Exception as e:
        logger.error(f"Error registering user {user.id}: {e}")
        # Continue anyway, the Web App will handle registration

    # Create keyboard with Web App button
    keyboard = [
        [KeyboardButton(
            text="💰 Apri Finance App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    # Welcome message
    welcome_message = (
        f"👋 Ciao {user.first_name}!\n\n"
        f"Benvenuto in **Scout Finance App**, il sistema di gestione finanziaria "
        f"per la cassa del tuo reparto scout.\n\n"
        f"📱 Clicca sul pulsante qui sotto per aprire l'app e iniziare a tracciare "
        f"le tue entrate, uscite e trasferimenti.\n\n"
        f"🎯 Funzionalità principali:\n"
        f"• 💰 Gestione saldi (contanti e conto)\n"
        f"• 📝 Tracciamento spese ed entrate\n"
        f"• 🔄 Trasferimenti tra conti\n"
        f"• 📊 Statistiche e analytics\n"
        f"• 📤 Export dati (CSV, Excel, PDF)\n"
        f"• 🏷️ Categorie personalizzabili\n"
        f"• 🌙 Dark mode\n\n"
        f"Usa /app in qualsiasi momento per riaprire l'applicazione."
    )

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /app command.
    Shows the Web App button to open the application.
    """
    user = update.effective_user

    logger.info(f"User {user.id} requested the app")

    # Create keyboard with Web App button
    keyboard = [
        [KeyboardButton(
            text="💰 Apri Finance App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        "📱 Clicca sul pulsante qui sotto per aprire Finance App:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "🤖 **Scout Finance Bot - Aiuto**\n\n"
        "**Comandi disponibili:**\n"
        "/start - Avvia il bot e registrati\n"
        "/app - Apri l'applicazione\n"
        "/help - Mostra questo messaggio di aiuto\n\n"
        "**Come usare l'app:**\n"
        "1. Clicca sul pulsante 'Apri Finance App'\n"
        "2. Imposta i tuoi saldi iniziali\n"
        "3. Inizia a tracciare le tue transazioni\n\n"
        "**Supporto:**\n"
        "Per problemi o domande, contatta il team di sviluppo."
    )

    await update.message.reply_text(
        help_text,
        parse_mode="Markdown"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Si è verificato un errore. Riprova più tardi."
        )


def main():
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables")
        return

    logger.info("Starting Scout Finance Bot...")
    logger.info(f"Backend API: {BACKEND_API_URL}")
    logger.info(f"Web App URL: {WEB_APP_URL}")

    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("app", app_command))
    application.add_handler(CommandHandler("help", help_command))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start bot
    if WEBHOOK_URL:
        # Webhook mode (for production)
        logger.info(f"Starting webhook mode: {WEBHOOK_URL}")
        port = int(os.getenv("PORT", 10000))
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TELEGRAM_BOT_TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}"
        )
    else:
        # Polling mode (for development)
        logger.info("Starting polling mode...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
