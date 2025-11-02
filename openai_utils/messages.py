import logging 
from openai import OpenAI 
from typing import Dict 

logger = logging.getLogger(__name__)


class Messages:
    def __init__(self , client : OpenAI ):
        self.client = client 

    def add_message(self , thread_id : str , content : str ) -> Dict | None:

        try:
            logger.info(f"Adding message to thread {thread_id}")
            message = self.client.beta.threads.messages.create(
                thread_id= thread_id , 
                role = "user",
                content = content
            )

            return message

        except Exception as e:
            logger.error(f"Error adding message to thread {thread_id}: {e}", exc_info=True)
            return None
