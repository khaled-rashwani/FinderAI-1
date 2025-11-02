from openai import OpenAI 
from typing import Dict
import logging 


logger = logging.getLogger(__name__)


class Threads:
    def __init__(self , client):
        self.client = client

    def create_thread(self) -> Dict:
        try:
            logger.info("Creating a new thread")
            user_thread = self.client.beta.threads.create()
            return user_thread
        
        except Exception as e : 
            logger.error(f"Error while creating thread: {e}", exc_info=True)
            return None
        