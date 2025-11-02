from .db_client import get_supabase_client
from typing import Optional 
import logging

logger = logging.getLogger(__name__)



async def get_user(user_id : str ) -> bool :

    client = get_supabase_client()

    if not client: 
        logger.error(f"Error in get_user : can't create a client")
        return False
    
    
    



