# import logging
# from telegram import User
# from .db_client import get_supabase_client
# # from constants.supabase_settings import USERS_TABLE, MESSAGES_TABLE
# from config import settings

# logger = logging.getLogger(__name__)


# async def get_or_create_user(user_data: User) -> tuple[dict | None, bool]:
#     client = await get_supabase_client()
#     if not client:
#         logger.error("Supabase client not available.")
#         return None, False

#     try:
#         response = await client.table(settings.SUPABASE_USERS_TABLE).select('*').eq('user_id', user_data.id).execute()

#         if response.data:
#             logger.info(f"User {user_data.id} found in database.")
#             return response.data[0], False

#         logger.info(f"User {user_data.id} not found. Creating new user.")
#         new_user = {
#             'user_id': user_data.id,
#             'first_name': user_data.first_name,
#             'last_name': user_data.last_name,
#             'username': user_data.username ,
#             'thread_id' : None
#         }
#         insert_response = await client.table(settings.SUPABASE_USERS_TABLE).insert(new_user).execute()

#         if insert_response.data:
#             logger.info(f"User {user_data.id} created successfully.")
#             return insert_response.data[0], True
#         else:
#             logger.error(f"Failed to create user {user_data.id}: {insert_response.error}")
#             return None, False

#     except Exception as e:
#         logger.error(f"Exception in get_or_create_user for {user_data.id}: {e}", exc_info=True)
#         return None, False


# async def update_user_thread(user_id : int , openai_thread_id : str) -> bool :

#     client = await get_supabase_client()

#     if not client:
#         logger.error(f"Supabase client not available for updating thread_id ")
#         return False
#     try:
#         await client.table(settings.SUPABASE_USERS_TABLE).update({'thread_id' : openai_thread_id}).eq('user_id' , user_id).execute()
#         logger.info(f"Successfully updated thread_id for user {user_id}")
#         return True

#     except Exception as e :
#         logger.error(f"Error Updating the thread for user {user_id} : {e}" , exc_info = True)
#         return False


# async def add_message(user_id, message_text, assistant_response=None, input_tokens=0, output_tokens=0):
#     """Adds a message record to the database."""
#     client = await get_supabase_client()
#     if not client:
#         logger.error("Supabase client not available.")
#         return False

#     try:
#         message_data = {
#             'user_id': user_id,
#             'message_text': message_text,
#             'assistant_response': assistant_response,
#             'input_tokens': input_tokens,
#             'output_tokens': output_tokens
#         }
#         await client.table(settings.SUPABASE_MESSAGES_TABLE).insert(message_data).execute()
#         logger.info(f"Message from user {user_id} saved successfully.")
#         return True
#     except Exception as e:
#         logger.error(f"Error saving message for user {user_id}: {e}", exc_info=True)
#         return False


import logging
from telegram import User
from .db_client import get_supabase_client
from config import settings

logger = logging.getLogger(__name__)


async def get_or_create_user(user_data: User) -> tuple[dict | None, bool]:
    client = get_supabase_client()
    if not client:
        logger.error("Supabase client not available.")
        return None, False

    try:
        response = (
            client.table(settings.SUPABASE_USERS_TABLE)
            .select("*")
            .eq("user_id", user_data.id)
            .execute()
        )

        if response.data:
            logger.info(f"User {user_data.id} found in database.")
            return response.data[0], False

        logger.info(f"User {user_data.id} not found. Creating new user.")
        new_user = {
            "user_id": user_data.id,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "username": user_data.username,
            "thread_id": None,
        }
        insert_response = (
            client.table(settings.SUPABASE_USERS_TABLE).insert(new_user).execute()
        )

        if insert_response.data:
            logger.info(f"User {user_data.id} created successfully.")
            return insert_response.data[0], True
        else:
            logger.error(
                f"Failed to create user {user_data.id}: {insert_response.error}"
            )
            return None, False

    except Exception as e:
        logger.error(
            f"Exception in get_or_create_user for {user_data.id}: {e}", exc_info=True
        )
        return None, False


async def update_user_thread_id(user_id: int, thread_id: str) -> bool:
    client = get_supabase_client()
    if not client:
        logger.error(f"Supabase client not available for updating thread_id")
        return False
    try:
        client.table(settings.SUPABASE_USERS_TABLE).update({"thread_id": thread_id}).eq(
            "user_id", user_id
        ).execute()
        logger.info(f"Successfully updated thread_id for user {user_id}")
        return True

    except Exception as e:
        logger.error(
            f"Error Updating the thread for user {user_id}: {e}", exc_info=True
        )
        return False


async def add_message(
    user_id, message_text, assistant_response=None, input_tokens=0, output_tokens=0
):
    client = get_supabase_client()
    if not client:
        logger.error("Supabase client not available.")
        return False

    try:
        message_data = {
            "user_id": user_id,
            "message_text": message_text,
            "assistant_response": assistant_response,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }
        client.table(settings.SUPABASE_MESSAGES_TABLE).insert(message_data).execute()
        logger.info(f"Message from user {user_id} saved successfully.")
        return True
    except Exception as e:
        logger.error(f"Error saving message for user {user_id}: {e}", exc_info=True)
        return False
