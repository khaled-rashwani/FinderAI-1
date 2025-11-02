import logging
import asyncio
import sys
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from config import settings
from telegram_utils import messages_handler, start_handler
from telegram_utils import error_handler  
from utils import health_check

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(), 
    ]
)

logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def setup_handlers(app):
    start_command_handler = CommandHandler('start', start_handler.handle_start_command)
    
    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        messages_handler.handle_text_message
    )

    voice_handler = MessageHandler(
        filters.VOICE ,
        messages_handler.handle_voice_message
    )
    
    non_text_handler = MessageHandler(
        filters.ALL & (~filters.TEXT),
        messages_handler.handle_non_text_message
    )
    
    app.add_handler(start_command_handler)
    app.add_handler(text_handler)
    app.add_handler(voice_handler)
    app.add_handler(non_text_handler)
    
    app.add_error_handler(error_handler.handle_error)
    
    logger.info("All handlers registered successfully.")


async def start_bot():
    logger.info("=" * 50)
    logger.info("Starting Athletes Hub Bot...")
    logger.info("=" * 50)
    
    health_check.initialize_health_status()
    
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    setup_handlers(app)
    
    asyncio.create_task(health_check.start_health_check_server(port=8080))
    
    logger.info("Bot is running and polling for updates...")
    logger.info("Health check available at: http://0.0.0.0:8080/health")
    logger.info("=" * 50)
    
    # Start polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True  
    )
    
    # Keep the bot running
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Received shutdown signal. Stopping bot...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        logger.info("Bot stopped gracefully.")


def main():
    try:
        settings.validate_enviroment_variables()
        logger.info("Environment variables validated successfully.")

        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Critical error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()







