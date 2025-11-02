import os
from dotenv import load_dotenv

load_dotenv()

# Telegram 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_USERS_TABLE = os.getenv("SUPABASE_USERS_TABLE")
SUPABASE_MESSAGES_TABLE = os.getenv("SUPABASE_MESSAGES_TABLE")

#OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")



def validate_enviroment_variables():
    required_vars = [
        TELEGRAM_BOT_TOKEN,
        SUPABASE_URL,
        SUPABASE_KEY,
        SUPABASE_USERS_TABLE,
        SUPABASE_MESSAGES_TABLE,
        OPENAI_API_KEY , 
        ASSISTANT_ID ,
    ]

    if not all(required_vars):
        raise ValueError("One or more enviroment variables are missing.")
