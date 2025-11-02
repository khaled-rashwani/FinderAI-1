
import logging 
from telegram import Update
from telegram.ext import ContextTypes
from constants import telegram_user_messages

logger = logging.getLogger(__name__)

async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command by sending welcome message.
    
    Args:
        update: Telegram update object
        context: Telegram context objec
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.first_name}) started the bot with /start command.")
    
    try:

        welcome_text = telegram_user_messages.WELCOME_MESSAGE.format(first_name = user.first_name)
        await update.message.reply_text(welcome_text)
        logger.info(f"Welcome message sent to user {user.id}")
    except Exception as e:
        logger.error(f"Error sending welcome message to user {user.id}: {e}", exc_info=True)