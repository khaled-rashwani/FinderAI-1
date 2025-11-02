import logging
from supabase import create_client, Client
from config import settings

logger = logging.getLogger(__name__)

supabase_client: Client | None = None


def initialize_supabase_client():
    """Initialize the Supabase client."""
    global supabase_client
    try:
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            supabase_client = create_client(
                settings.SUPABASE_URL, settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized successfully.")
        else:
            logger.warning(
                "Supabase URL or Key not found. Supabase client not initialized."
            )
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {e}", exc_info=True)
        supabase_client = None


def get_supabase_client():
    """Get the Supabase client, initializing it if necessary."""
    global supabase_client
    if supabase_client is None:
        initialize_supabase_client()
    return supabase_client
