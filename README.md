# Telegram Bot with Supabase Integration

A sophisticated Telegram bot that integrates with Supabase for data persistence and uses OpenAI's GPT models for intelligent conversations. The bot supports both text and voice messages, with automatic speech-to-text transcription.

## Features

- 🤖 **Intelligent Chat**: Powered by OpenAI's GPT-4o-mini model with conversation history
- 🎤 **Voice Message Support**: Automatic speech-to-text transcription using OpenAI Whisper
- 💾 **Data Persistence**: User data and conversation history stored in Supabase
- 🔄 **Conversation Memory**: Maintains context across multiple messages
- 🛠️ **MCP Tools Integration**: Extensible with Model Context Protocol tools
- 📊 **Health Monitoring**: Built-in health check endpoint for monitoring
- 🔒 **User Management**: Automatic user registration and data tracking
- ⚡ **Async Architecture**: High-performance asynchronous processing

## Architecture

```
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py         # Environment variables and settings
├── constants/              # Application constants
│   ├── prompts.py          # System prompts and templates
│   ├── supabase_settings.py
│   └── telegram_user_messages.py
├── langchain_router/       # AI agent routing
│   └── agent.py           # LangGraph agent implementation
├── supabase_utils/         # Database operations
│   ├── db_client.py       # Supabase client management
│   ├── db_read.py         # Database read operations
│   ├── db_write.py        # Database write operations
│   ├── create-users-table.sql
│   └── create-messages-table.sql
├── telegram_utils/         # Telegram bot handlers
│   ├── error_handler.py   # Error handling
│   ├── messages_handler.py # Message processing
│   ├── openai_speech_to_text.py # Voice transcription
│   └── start_handler.py   # Start command handler
├── utils/                  # Utility functions
│   └── health_check.py    # Health monitoring
└── main.py                # Application entry point
```

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Supabase account and project
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd telegram-and-supabase
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Telegram Bot Configuration
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_anon_key_here
   SUPABASE_USERS_TABLE=users
   SUPABASE_MESSAGES_TABLE=messages
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Set up Supabase database**
   Run the SQL scripts in the `supabase_utils/` directory to create the required tables:
   - `create-users-table.sql`
   - `create-messages-table.sql`

## Usage

1. **Start the bot**
   ```bash
   python main.py
   ```

2. **Health Check**
   The bot includes a health check endpoint available at:
   ```
   http://localhost:8080/health
   ```

3. **Interact with the bot**
   - Send `/start` to begin
   - Send text messages for AI responses
   - Send voice messages for speech-to-text processing

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Yes |
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anon key | Yes |
| `SUPABASE_USERS_TABLE` | Users table name | Yes |
| `SUPABASE_MESSAGES_TABLE` | Messages table name | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Database Schema

**Users Table:**
- `user_id` (bigint, primary key)
- `first_name` (text)
- `last_name` (text)
- `username` (text)
- `created_at` (timestamp)

**Messages Table:**
- `id` (serial, primary key)
- `user_id` (bigint, foreign key)
- `message_text` (text)
- `assistant_response` (text)
- `input_tokens` (integer)
- `output_tokens` (integer)
- `sent_at` (timestamp)

## Features in Detail

### Voice Message Processing
- Automatically detects voice messages
- Converts OGG audio to WAV format
- Handles stereo to mono conversion
- Uses OpenAI Whisper for transcription
- Processes transcribed text as regular messages

### Conversation Memory
- Maintains conversation history for each user
- Retrieves last 5 messages for context
- Stores both user messages and bot responses
- Tracks token usage for cost monitoring

### Error Handling
- Comprehensive error logging
- User-friendly error messages
- Graceful degradation on service failures
- Health status monitoring

### Performance Optimizations
- Async/await throughout
- User-level locking to prevent concurrent processing
- TTL cache for user locks
- Efficient database queries

## Development

### Project Structure
The project follows a modular architecture with clear separation of concerns:

- **Config**: Environment and settings management
- **Constants**: Application-wide constants and messages
- **LangChain Router**: AI agent and conversation logic
- **Supabase Utils**: Database operations and client management
- **Telegram Utils**: Bot handlers and message processing
- **Utils**: Health monitoring and utility functions

### Adding New Features
1. Create handlers in `telegram_utils/`
2. Add database operations in `supabase_utils/`
3. Update constants in `constants/`
4. Modify the main application in `main.py`

## Monitoring

The bot includes comprehensive logging and health monitoring:

- Structured logging with different levels
- Health check endpoint for uptime monitoring
- Component status tracking
- Error reporting and debugging information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions, please open an issue in the repository or contact the development team.
