import logging 
from openai import AssistantEventHandler , OpenAI
from openai.types.beta.threads import Run


logger = logging.getLogger(__name__)



class Runs:
    def __init__(self , client : OpenAI):
        self.client = client 

    def run_stream(self , thread_id : str , assistant_id : str , event_handler = AssistantEventHandler) -> Run | None:
        try : 

            logger.info(f"Starting a new run on thread {thread_id} with assistant {assistant_id}")
            with self.client.beta.threads.runs.stream(
                assistant_id = assistant_id , 
                thread_id = thread_id , 
                event_handler = event_handler
            ) as stream:
                stream.until_done()
                final_run = stream.get_final_run()
            
            logger.info(f"Stream completed for run on thread {thread_id} , Run Status : {final_run.status}")
            return final_run


        except Exception as e : 
            logger.error(f"Error during streaming run for thread {thread_id}: {e}", exc_info=True)
            return None


    