from .messages import Messages
from .threads import Threads 
from .response_handler import ResponseHandler
from .runs import Runs
from openai import OpenAI
from config import settings
import logging 
from typing import Tuple

logger = logging.getLogger(__name__)

class AssistantManger:

    def __init__(self , client : OpenAI ):
        self.client = client
        self.assistant_id = settings.ASSISTANT_ID

        self.threads = Threads(self.client)
        self.messages = Messages(self.client)
        self.runs = Runs(self.client)

    def get_response(self , thread_id : str , message_content : str ) -> Tuple[str | None , int , int ]:


        logger.info(f"Orchestrating response for thread_id: {thread_id}")

        try: 
            create_message = self.messages.add_message(thread_id=thread_id, content=message_content)
            if not create_message: 
                return "Failed to add message.", 0, 0 
            
            response_handler = ResponseHandler()
            
            final_run = self.runs.run_stream(thread_id, self.assistant_id, response_handler)
            
            final_response = response_handler.current_response
            logger.info(f"Final response captured for thread {thread_id}: '{final_response[:70]}...'")

            if final_run and final_run.usage:
                input_tokens = final_run.usage.prompt_tokens
                output_tokens = final_run.usage.completion_tokens
                logger.info(f"Token usage for run {final_run.id}: Input={input_tokens}, Output={output_tokens}")
                return final_response, input_tokens, output_tokens
            else:
                logger.warning("Could not retrieve token usage information.")
                return final_response, 0, 0
        
        except Exception as e : 
            logger.error(f"Error while getting response for thread {thread_id} : {e}")
            return f"An error occurred : {str(e)}" , 0 , 0 



