import logging 
from .db_client import get_supabase_client 
from constants.supabase_settings import MAX_MESSAGES_TO_RETRIEVE
from config import settings

logger = logging.getLogger(__name__)



async def get_last_five_messages(user_id : int ) -> list:

    client = get_supabase_client()
    if not client: 
        logger.error("Supabase client not available.")
        return[]

    try: 
        response = (
            client.table(settings.SUPABASE_MESSAGES_TABLE)
            .select('message_text , assistant_response')
            .eq('user_id',user_id)
            .order('sent_at',desc=True)
            .limit(MAX_MESSAGES_TO_RETRIEVE)
            .execute()
        )

        if response.data:
            logger.info(f"Retrieved{len(response.data)} messages for user {user_id}")
            return response.data
        
        return []
    

    except Exception as e : 
        logger.error(f"Error fetching messages for user {user_id} : {e}",exc_info = True)
        return[]

