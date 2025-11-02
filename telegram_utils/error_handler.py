import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes
from constants import telegram_user_messages

logger = logging.getLogger(__name__)

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        f"Exception while handling an update: {context.error}",
        exc_info=context.error
    )    
    if update:
        logger.error(f"Update that caused error: {update}")
    
    try:
        if update and update.effective_message:
            error_message = telegram_user_messages.GENERAL_ERROR_MESSAGE
            
            await update.effective_message.reply_text(error_message)
            logger.info(f"Error message sent to user {update.effective_user.id if update.effective_user else 'unknown'}")
    
    except Exception as e:
        logger.error(f"Could not send error message to user: {e}", exc_info=True)



def log_system_error(error_type: str, error: Exception, context: str = None):
    error_msg = f"[{error_type}] System error"
    if context:
        error_msg += f" in {context}"
    error_msg += f": {error}"
    
    logger.error(error_msg, exc_info=error)