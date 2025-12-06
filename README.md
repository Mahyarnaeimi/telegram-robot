# Simple Telegram Bot

A feature-rich Telegram bot built with Python and python-telegram-bot library. Clean architecture with OOP design, perfect for learning or as a starter template.

## Features

- Command handlers (`/start`, `/help`, `/info`, `/quote`, `/menu`, `/stats`, `/echo`)
- Interactive inline keyboards with callbacks
- User data tracking and statistics
- Async/await support for better performance
- Comprehensive logging (file + console)
- Error handling
- Clean OOP architecture

## Installation

### Prerequisites

- Python 3.10+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegram-robot.git
   cd telegram-robot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and show welcome message |
| `/help` | Display available commands |
| `/info` | Show bot information |
| `/quote` | Get a random inspirational quote |
| `/menu` | Show interactive menu with buttons |
| `/stats` | Display your usage statistics |
| `/echo <text>` | Echo back your message |

## Project Structure

```
telegram-robot/
├── bot.py           # Main bot logic
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
├── .env.example     # Environment template
├── .gitignore       # Git ignore rules
└── README.md        # Documentation
```

## Configuration

All settings can be configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | Required |
| `BOT_NAME` | Bot display name | Simple Telegram Bot |
| `ADMIN_IDS` | Admin user IDs (comma-separated) | - |
| `LOG_LEVEL` | Logging level | INFO |
| `LOG_FILE` | Log file path | bot.log |

## Usage Example

```python
from bot import TelegramBot

bot = TelegramBot(token="your_token")
bot.run()
```

## Tech Stack

- **Python 3.10+**
- **python-telegram-bot** - Telegram Bot API wrapper
- **python-dotenv** - Environment variable management

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request
