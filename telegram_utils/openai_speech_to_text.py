import logging
from openai import AsyncOpenAI
from config import settings
from typing import BinaryIO

logger = logging.getLogger(__name__)

try:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    logger.info("AsyncOpenAI client for speech services initialized successfully.")

except Exception as e:
    client = None
    logger.error(f"Failed to initialize AsyncOpenAI client : {e}", exc_info=True)


async def speech_to_text_from_file_obj(audio_file: BinaryIO) -> str | None:

    if not client:
        logger.error("OpenAI client is not available. Cannot transcribe audio.")
        return None

    try:
        logger.info(f"Transcribing audio file from in-memory object: {audio_file.name}")

        transcript_response = await client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )

        transcribed_text = transcript_response.text
        logger.info(
            f"Audio transcribed successfully. Result: '{transcribed_text[:50]}...'"
        )
        return transcribed_text

    except Exception as e:
        logger.error(
            f"An error occurred during audio transcription: {e}", exc_info=True
        )
        return None
