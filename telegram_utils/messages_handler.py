# import asyncio
# import logging 
# from telegram import Update, constants
# from telegram.ext import ContextTypes
# from cachetools import TTLCache

# from constants import telegram_user_messages
# from supabase_utils import db_write
# from openai_utils import AssistantManger
# from openai import OpenAI 
# from config import settings

# import sys , os 
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import io
# import requests
# import soundfile as sf
# import numpy as np
# from telegram_utils import openai_speech_to_text



# logger = logging.getLogger(__name__)


# try: 
#     openai_client = OpenAI(api_key= settings.OPENAI_API_KEY)
#     assistant_manager = AssistantManger(client= openai_client)
#     logger.info("OpenAI client and assistant manger are init ")

# except Exception as e: 
#     assistant_manager = None
#     logger.critical(f"Failed to init the assistant manger {e}" , exc_info = True )


# CACHE_MAX_SIZE = 2000
# CACHE_TTL_SECONDS = 600
# user_locks = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

# def _get_user_lock(user_id):
#     try: 
#         lock = user_locks[user_id]
#         logger.debug(f"Lock for user {user_id} found in cache.")
#         return lock
#     except KeyError: 
#         logger.debug(f"Lock for user {user_id} not in cache. Creating new lock.")
#         new_lock = asyncio.Lock()
#         user_locks[user_id] = new_lock
#         return new_lock

# async def _send_typing_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Send typing action to show bot is processing."""
#     try:
#         await context.bot.send_chat_action(
#             chat_id=update.effective_chat.id,
#             action=constants.ChatAction.TYPING
#         )
#     except Exception as e:
#         logger.error(f"Error sending typing action: {e}")


# async def _keep_typing_until_done(update: Update, context: ContextTypes.DEFAULT_TYPE, task):
#     """
#     Keep sending typing action while waiting for the task to complete.
#     """
#     typing_task = asyncio.create_task(_continuous_typing(update, context))
    
#     try:
#         result = await task
#         return result
#     except Exception as e:
#         logger.error(f"Error during task execution: {e}", exc_info=True)
#         raise
#     finally:
#         typing_task.cancel()
#         try:
#             await typing_task
#         except asyncio.CancelledError:
#             pass


# # async def _continuous_typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     """Send typing action continuously every 4 seconds."""
# #     try:
# #         while True:
# #             await context.bot.send_chat_action(
# #                 chat_id=update.effective_chat.id,
# #                 action=constants.ChatAction.TYPING
# #             )
# #             await asyncio.sleep(4) 
# #     except asyncio.CancelledError:
# #         logger.debug("Continuous typing cancelled.")
# #         raise
# #     except Exception as e:
# #         logger.error(f"Error in continuous typing: {e}")

# async def _continuous_typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Send typing action continuously every 4 seconds."""
#     try:
#         while True:
#             await context.bot.send_chat_action(
#                 chat_id=update.effective_chat.id,
#                 action=constants.ChatAction.TYPING
#             )
#             await asyncio.sleep(4) 
#     except asyncio.CancelledError:
#         logger.debug("Continuous typing cancelled.")
#         raise
#     except Exception as e:
#         logger.error(f"Error in continuous typing: {e}")



# async def _get_or_create_thread_id_for_user(user_id : int , current_thread_id : str | None ) -> str | None :

#     if current_thread_id: 
#         logger.info(f"Found existing thread_id for user {user_id}: {current_thread_id}")
#         return current_thread_id
    

#     logger.info(f"No thread_id found for user {user_id}. Creating a new one.")
#     new_thread = assistant_manager.threads.create_thread()

#     if new_thread: 
#         await db_write.update_user_thread(user_id = user_id , openai_thread_id= new_thread.id)
#         return new_thread.id
    
#     else: 
#         logger.error(f"Error when create thread for user {user_id}")
#         return None 



# # async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     message_text = update.message.text
# #     logger.info(f"Received message from user {user.id} ({user.first_name}): '{message_text[:50]}...'")
    
# #     if not assistant_manager:
# #         logger.error("AssistantManager is not available. Cannot process message.")
# #         await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
# #         return

# #     user_lock = _get_user_lock(user.id)
    
# #     async with user_lock:
# #         try:
# #             await _send_typing_action(update, context)
            
# #             db_user, is_new = await db_write.get_or_create_user(user)

# #             if not db_user:
# #                 logger.error(f"Failed to get or create user {user.id} in the database")
# #                 await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
# #                 return
            
# #             if is_new:
# #                 logger.info(f"New user {user.id} ({user.first_name}) has been created in the database")

# #             thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('openai_thread_id'))

# #             if not thread_id:
# #                 await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
# #                 return

# #             assistant_response_text, input_tokens, output_tokens = assistant_manager.get_response(
# #                 thread_id,
# #                 message_text
# #             )
            
# #             success = await db_write.add_message(
# #                 user_id=user.id,
# #                 message_text=message_text,
# #                 assistant_response=assistant_response_text,
# #                 input_tokens=input_tokens,
# #                 output_tokens=output_tokens
# #             )
            
# #             if not success:
# #                 logger.warning(f"Failed to save message for user {user.id} to the database.")

# #             await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
# #             logger.info(f"Successfully responded to user {user.id}")
            
# #         except Exception as e:
# #             logger.error(
# #                 f"Unexpected error handling message from user {user.id}: {e}",
# #                 exc_info=True
# #             )
# #             await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)

# # async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     user = update.effective_user
# #     logger.info(f"Received voice message from user {user.id} ({user.first_name})")

# #     if not assistant_manager:
# #         logger.error("AssistantManager is not available. Cannot process message.")
# #         await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
# #         return

# #     user_lock = _get_user_lock(user.id)
# #     async with user_lock:
# #         try:
# #             await _send_typing_action(update, context)
            
# #             voice_file = await context.bot.get_file(update.message.voice.file_id)
# #             file_url = voice_file.file_path
# #             logger.info(f"Downloading voice file from URL: {file_url}")

# #             response = requests.get(file_url)
# #             response.raise_for_status() 
# #             ogg_audio_data = io.BytesIO(response.content)

# #             audio_data, sample_rate = sf.read(ogg_audio_data)
            
# #             if audio_data.ndim > 1:
# #                 logger.debug("Audio is stereo, converting to mono.")
# #                 audio_data = np.mean(audio_data, axis=1)
                
# #             wav_in_memory_file = io.BytesIO()
# #             sf.write(wav_in_memory_file, audio_data, sample_rate, format='WAV', subtype='PCM_16')
# #             wav_in_memory_file.seek(0) 

# #             wav_in_memory_file.name = "voice.wav"
# #             transcribed_text = await openai_speech_to_text.speech_to_text_from_file_obj(wav_in_memory_file)

# #             if not transcribed_text:
# #                 await update.message.reply_text(telegram_user_messages.VOICE_TRANSCRIPTION_FAILED_MESSAGE)
# #                 return 
            
# #             logger.info(f"Transcribed text for user {user.id}: '{transcribed_text}'")

# #             db_user, _ = await db_write.get_or_create_user(user)
# #             thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('thread_id'))
            
# #             if not thread_id:
# #                 await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
# #                 return

# #             assistant_response_text, input_tokens, output_tokens = assistant_manager.get_response(
# #                 thread_id,
# #                 transcribed_text
# #             )

# #             success = await db_write.add_message(
# #                 user_id = user.id,
# #                 message_text = f"[VOICE]: {transcribed_text}",
# #                 assistant_response = assistant_response_text, 
# #                 input_tokens = input_tokens, 
# #                 output_tokens = output_tokens
# #             )

# #             if not success: 
# #                 logger.warning(f"Failed to save transcribed voice message for user {user.id}")

# #             await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
# #             logger.info(f"Successfully responded to voice message from user {user.id}")

# #         except Exception as e:
# #             logger.error(f"Error handling voice message for user {user.id}: {e}", exc_info=True)
# #             await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)

# async def _run_with_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, task):
#     """
#     Run a task while continuously sending a 'typing' action.
#     """
#     typing_task = asyncio.create_task(_continuous_typing(update, context))
#     try:
#         return await task
#     finally:
#         typing_task.cancel()
#         try:
#             await typing_task
#         except asyncio.CancelledError:
#             pass

# async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     message_text = update.message.text
#     logger.info(f"Received message from user {user.id} ({user.first_name}): '{message_text[:50]}...'")
    
#     if not assistant_manager:
#         logger.error("AssistantManager is not available. Cannot process message.")
#         await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
#         return

#     user_lock = _get_user_lock(user.id)
    
#     async with user_lock:
#         try:
#             db_user, is_new = await db_write.get_or_create_user(user)
#             if not db_user:
#                 logger.error(f"Failed to get or create user {user.id} in the database")
#                 await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
#                 return
            
#             if is_new:
#                 logger.info(f"New user {user.id} ({user.first_name}) has been created in the database")

#             # <-- تأكد من استخدام اسم الحقل الصحيح 'thread_id'
#             thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('openai_thread_id'))
#             if not thread_id:
#                 await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
#                 return

#             # <-- هنا نعيد استخدام دالة الـ typing
#             response_task = assistant_manager.get_response(thread_id, message_text)
#             assistant_response_text, input_tokens, output_tokens = await _run_with_typing(update, context, response_task)
            
#             success = await db_write.add_message(
#                 user_id=user.id,
#                 message_text=message_text,
#                 assistant_response=assistant_response_text,
#                 input_tokens=input_tokens,
#                 output_tokens=output_tokens
#             )
            
#             if not success:
#                 logger.warning(f"Failed to save message for user {user.id} to the database.")

#             await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
#             logger.info(f"Successfully responded to user {user.id}")
            
#         except Exception as e:
#             logger.error(f"Unexpected error handling message from user {user.id}: {e}", exc_info=True)
#             await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)

# async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     logger.info(f"Received voice message from user {user.id} ({user.first_name})")

#     if not assistant_manager:
#         logger.error("AssistantManager is not available. Cannot process message.")
#         await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
#         return

#     user_lock = _get_user_lock(user.id)
#     async with user_lock:
#         try:
#             # <-- دمجنا دالة الـ typing هنا أيضاً
#             async def full_voice_process():
#                 voice_file = await context.bot.get_file(update.message.voice.file_id)
#                 file_url = voice_file.file_path
#                 logger.info(f"Downloading voice file from URL: {file_url}")

#                 response = requests.get(file_url)
#                 response.raise_for_status() 
#                 ogg_audio_data = io.BytesIO(response.content)

#                 audio_data, sample_rate = sf.read(ogg_audio_data)
#                 if audio_data.ndim > 1:
#                     audio_data = np.mean(audio_data, axis=1)
                    
#                 wav_in_memory_file = io.BytesIO()
#                 sf.write(wav_in_memory_file, audio_data, sample_rate, format='WAV', subtype='PCM_16')
#                 wav_in_memory_file.seek(0) 
#                 wav_in_memory_file.name = "voice.wav"
                
#                 transcribed_text = await openai_speech_to_text.speech_to_text_from_file_obj(wav_in_memory_file)
#                 if not transcribed_text:
#                     await update.message.reply_text(telegram_user_messages.VOICE_TRANSCRIPTION_FAILED_MESSAGE)
#                     return None, None, None, None
                
#                 logger.info(f"Transcribed text for user {user.id}: '{transcribed_text}'")

#                 db_user, _ = await db_write.get_or_create_user(user)
#                 # <-- تأكد من استخدام اسم الحقل الصحيح 'thread_id'
#                 thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('openai_thread_id'))
#                 if not thread_id:
#                     await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
#                     return None, None, None, None

#                 response_text, input_tokens, output_tokens = assistant_manager.get_response(thread_id, transcribed_text)
#                 return transcribed_text, response_text, input_tokens, output_tokens

#             transcribed_text, assistant_response_text, input_tokens, output_tokens = await _run_with_typing(update, context, full_voice_process())

#             if assistant_response_text is None:
#                 return # تم التعامل مع الخطأ داخل الدالة

#             success = await db_write.add_message(
#                 user_id=user.id,
#                 message_text=f"[VOICE]: {transcribed_text}",
#                 assistant_response=assistant_response_text, 
#                 input_tokens=input_tokens, 
#                 output_tokens=output_tokens
#             )

#             if not success: 
#                 logger.warning(f"Failed to save transcribed voice message for user {user.id}")

#             await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
#             logger.info(f"Successfully responded to voice message from user {user.id}")

#         except Exception as e:
#             logger.error(f"Error handling voice message for user {user.id}: {e}", exc_info=True)
#             await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)


# async def handle_non_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Handle non-text messages (photos, stickers, etc.).
#     """
#     user = update.effective_user
#     logger.info(f"Received a non-text message from user {user.id} ({user.first_name}).")
    
#     try:
#         await update.message.reply_text(telegram_user_messages.UNSUPPORTED_MESSAGE_TYPE_REPLY)
#     except Exception as e:
#         logger.error(f"Error handling non-text message from user {user.id}: {e}")

import asyncio
import logging 
from telegram import Update, constants
from telegram.ext import ContextTypes
from cachetools import TTLCache

from constants import telegram_user_messages
from supabase_utils import db_write
from openai_utils import AssistantManger
from openai import OpenAI 
from config import settings

import io
import requests
import soundfile as sf
import numpy as np
from telegram_utils import openai_speech_to_text

logger = logging.getLogger(__name__)

# Lazy initialization - clients will be created on first use
_openai_client: OpenAI | None = None
_assistant_manager: AssistantManger | None = None

def _get_assistant_manager() -> AssistantManger | None:
    """Get or initialize the assistant manager lazily."""
    global _openai_client, _assistant_manager
    if _assistant_manager is None:
        try:
            _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            _assistant_manager = AssistantManger(client=_openai_client)
            logger.info("OpenAI client and assistant manager are initialized.")
        except Exception as e:
            logger.critical(f"Failed to initialize the assistant manager: {e}", exc_info=True)
            return None
    return _assistant_manager


CACHE_MAX_SIZE = 2000
CACHE_TTL_SECONDS = 600
user_locks = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

def _get_user_lock(user_id):
    try: 
        lock = user_locks[user_id]
        logger.debug(f"Lock for user {user_id} found in cache.")
        return lock
    except KeyError: 
        logger.debug(f"Lock for user {user_id} not in cache. Creating new lock.")
        new_lock = asyncio.Lock()
        user_locks[user_id] = new_lock
        return new_lock

async def _run_with_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, task):
    typing_task = asyncio.create_task(_continuous_typing(update, context))
    try:
        return await task
    finally:
        typing_task.cancel()
        try:
            await typing_task
        except asyncio.CancelledError:
            pass

async def _continuous_typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        while True:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=constants.ChatAction.TYPING
            )
            await asyncio.sleep(4) 
    except asyncio.CancelledError:
        logger.debug("Continuous typing cancelled.")
        raise
    except Exception as e:
        logger.error(f"Error in continuous typing: {e}")

async def _get_or_create_thread_id_for_user(user_id: int, current_thread_id: str | None) -> str | None:
    if current_thread_id: 
        logger.info(f"Found existing thread_id for user {user_id}: {current_thread_id}")
        return current_thread_id
    
    assistant_manager = _get_assistant_manager()
    if not assistant_manager:
        logger.error("AssistantManager is not available. Cannot create thread.")
        return None
    
    logger.info(f"No thread_id found for user {user_id}. Creating a new one.")
    new_thread = assistant_manager.threads.create_thread()

    if new_thread: 
        # <-- تم توحيد اسم الدالة والبارامترات
        await db_write.update_user_thread_id(user_id=user_id, thread_id=new_thread.id)
        return new_thread.id
    else: 
        logger.error(f"Error when creating a thread for user {user_id}")
        return None 

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    logger.info(f"Received message from user {user.id} ({user.first_name}): '{message_text[:50]}...'")
    
    assistant_manager = _get_assistant_manager()
    if not assistant_manager:
        logger.error("AssistantManager is not available. Cannot process message.")
        await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
        return

    user_lock = _get_user_lock(user.id)
    
    async with user_lock:
        try:
            db_user, is_new = await db_write.get_or_create_user(user)
            if not db_user:
                logger.error(f"Failed to get or create user {user.id} in the database")
                await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
                return
            
            if is_new:
                logger.info(f"New user {user.id} ({user.first_name}) has been created in the database")

            # <-- تم توحيد اسم الحقل
            thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('thread_id'))
            if not thread_id:
                await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
                return

            response_coro = asyncio.to_thread(
                assistant_manager.get_response,
                thread_id,
                message_text
            )
            assistant_response_text, input_tokens, output_tokens = await _run_with_typing(update, context, response_coro)
            
            success = await db_write.add_message(
                user_id=user.id,
                message_text=message_text,
                assistant_response=assistant_response_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            if not success:
                logger.warning(f"Failed to save message for user {user.id} to the database.")

            await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
            logger.info(f"Successfully responded to user {user.id}")
            
        except Exception as e:
            logger.error(f"Unexpected error handling message from user {user.id}: {e}", exc_info=True)
            await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)



async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # logger.info(f"Received voice message from user {user.id} ({user.first_name})")
    logger.info(f"Received voice message from user {user.id} ({user.first_name})")

    assistant_manager = _get_assistant_manager()
    if not assistant_manager:
        logger.error("AssistantManager is not available. Cannot process message.")
        await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
        return

    user_lock = _get_user_lock(user.id)
    async with user_lock:
        try:
            # Capture assistant_manager for use in inner function
            manager = assistant_manager
            async def full_voice_process():
                voice_file = await context.bot.get_file(update.message.voice.file_id)
                file_url = voice_file.file_path
                logger.info(f"Downloading voice file from URL: {file_url}")

                response = requests.get(file_url)
                response.raise_for_status() 
                ogg_audio_data = io.BytesIO(response.content)

                audio_data, sample_rate = sf.read(ogg_audio_data)
                if audio_data.ndim > 1:
                    audio_data = np.mean(audio_data, axis=1)
                    
                wav_in_memory_file = io.BytesIO()
                sf.write(wav_in_memory_file, audio_data, sample_rate, format='WAV', subtype='PCM_16')
                wav_in_memory_file.seek(0) 
                wav_in_memory_file.name = "voice.wav"
                
                transcribed_text = await openai_speech_to_text.speech_to_text_from_file_obj(wav_in_memory_file)
                if not transcribed_text:
                    await update.message.reply_text(telegram_user_messages.VOICE_TRANSCRIPTION_FAILED_MESSAGE)
                    return None, None, None, None
                
                logger.info(f"Transcribed text for user {user.id}: '{transcribed_text}'")

                db_user, _ = await db_write.get_or_create_user(user)
                # <-- تم توحيد اسم الحقل
                thread_id = await _get_or_create_thread_id_for_user(user.id, db_user.get('thread_id'))
                if not thread_id:
                    await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)
                    return None, None, None, None

                response_text, input_tokens, output_tokens = await asyncio.to_thread(
                    manager.get_response,
                    thread_id,
                    transcribed_text
                )
                return transcribed_text, response_text, input_tokens, output_tokens

            transcribed_text, assistant_response_text, input_tokens, output_tokens = await _run_with_typing(update, context, full_voice_process())

            if assistant_response_text is None:
                return

            success = await db_write.add_message(
                user_id=user.id,
                message_text=f"[VOICE]: {transcribed_text}",
                assistant_response=assistant_response_text, 
                input_tokens=input_tokens, 
                output_tokens=output_tokens
            )

            if not success: 
                logger.warning(f"Failed to save transcribed voice message for user {user.id}")

            await update.message.reply_text(assistant_response_text, parse_mode="Markdown")
            logger.info(f"Successfully responded to voice message from user {user.id}")

        except Exception as e:
            logger.error(f"Error handling voice message for user {user.id}: {e}", exc_info=True)
            await update.message.reply_text(telegram_user_messages.GENERAL_ERROR_MESSAGE)

async def handle_non_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Received a non-text message from user {user.id} ({user.first_name}).")
    try:
        await update.message.reply_text(telegram_user_messages.UNSUPPORTED_MESSAGE_TYPE_REPLY)
    except Exception as e:
        logger.error(f"Error handling non-text message from user {user.id}: {e}")