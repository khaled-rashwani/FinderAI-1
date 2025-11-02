import logging
from openai import OpenAI , AssistantEventHandler 
from typing import List , Tuple 


from .threads import Threads 
from .messages import Messages
from .runs import Runs



class ResponseHandler(AssistantEventHandler):

    def __init__(self):
        super().__init__()
        self._response_parts : List[str] = []

    def on_text_delta(self , delta , snapshot):
        self._response_parts.append(delta.value)


    @property
    def current_response(self) -> str:
        return "".join(self._response_parts)
    
