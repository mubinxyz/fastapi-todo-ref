# telegram_bot/bot.py
from telegram.ext import ApplicationBuilder, ContextTypes
from core.config import settings

# Initialize the application without the default updater
application = (
    ApplicationBuilder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .updater(None) 
    .build()
)

def register_handlers():
    # Import here to avoid circular imports
    from telegram_bot.handlers import start, add_todo, list_todos
    from telegram.ext import CommandHandler

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_todo))
    application.add_handler(CommandHandler("list", list_todos))