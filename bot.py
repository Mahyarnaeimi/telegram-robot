"""
Simple Telegram Bot
A feature-rich Telegram bot with commands, inline keyboards, and user management.

Features:
- Command handlers (/start, /help, /info, /weather, /quote)
- Inline keyboards and callbacks
- User state management
- Error handling and logging
- Async/await support
"""

import os
import logging
import random
from datetime import datetime
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Bot token from environment
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Conversation states
CHOOSING, TYPING_REPLY = range(2)

# Sample data
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
    "The best error message is the one that never shows up. - Thomas Fuchs",
    "Simplicity is the soul of efficiency. - Austin Freeman",
]

# Store user data
user_data_store = {}


class TelegramBot:
    """Main Telegram Bot class"""

    def __init__(self, token: str):
        """Initialize the bot with token"""
        if not token:
            raise ValueError("Bot token is required. Set TELEGRAM_BOT_TOKEN in .env file")

        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("quote", self.quote_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("echo", self.echo_command))

        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

        # Message handler for regular messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Error handler
        self.application.add_error_handler(self.error_handler)

        logger.info("All handlers registered successfully")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id

        # Store user data
        if user_id not in user_data_store:
            user_data_store[user_id] = {
                'username': user.username,
                'first_name': user.first_name,
                'joined': datetime.now().isoformat(),
                'message_count': 0
            }

        welcome_message = (
            f"Hello {user.first_name}! Welcome to the bot.\n\n"
            f"I'm a simple but powerful Telegram bot.\n"
            f"Use /help to see available commands.\n\n"
            f"Created with Python + python-telegram-bot"
        )

        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("Help", callback_data="help"),
                InlineKeyboardButton("Info", callback_data="info"),
            ],
            [
                InlineKeyboardButton("Get Quote", callback_data="quote"),
                InlineKeyboardButton("Stats", callback_data="stats"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        logger.info(f"User {user.username} ({user_id}) started the bot")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = (
            "Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/info - Show bot information\n"
            "/quote - Get a random quote\n"
            "/menu - Show interactive menu\n"
            "/stats - Show your statistics\n"
            "/echo <text> - Echo your message\n\n"
            "You can also send me any message and I'll respond!"
        )
        await update.message.reply_text(help_text)

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /info command"""
        info_text = (
            "Bot Information\n"
            "---------------\n"
            f"Bot Name: Simple Telegram Bot\n"
            f"Version: 1.0.0\n"
            f"Python: 3.10+\n"
            f"Library: python-telegram-bot\n"
            f"Total Users: {len(user_data_store)}\n"
            f"Server Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "GitHub: github.com/yourusername/telegram-bot"
        )
        await update.message.reply_text(info_text)

    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /quote command - send a random quote"""
        quote = random.choice(QUOTES)
        await update.message.reply_text(f"\"{quote}\"")

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /menu command - show interactive menu"""
        keyboard = [
            [
                InlineKeyboardButton("Random Quote", callback_data="quote"),
                InlineKeyboardButton("Bot Info", callback_data="info"),
            ],
            [
                InlineKeyboardButton("My Stats", callback_data="stats"),
                InlineKeyboardButton("Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton("Visit GitHub", url="https://github.com"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /stats command - show user statistics"""
        user_id = update.effective_user.id

        if user_id in user_data_store:
            data = user_data_store[user_id]
            stats_text = (
                "Your Statistics\n"
                "---------------\n"
                f"Username: @{data.get('username', 'N/A')}\n"
                f"Name: {data.get('first_name', 'N/A')}\n"
                f"Joined: {data.get('joined', 'N/A')}\n"
                f"Messages Sent: {data.get('message_count', 0)}\n"
            )
        else:
            stats_text = "No data found. Send /start first!"

        await update.message.reply_text(stats_text)

    async def echo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /echo command - echo user's message"""
        if context.args:
            text = ' '.join(context.args)
            await update.message.reply_text(f"Echo: {text}")
        else:
            await update.message.reply_text("Usage: /echo <your message>")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button callbacks"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        callback_data = query.data

        if callback_data == "help":
            text = (
                "Available Commands:\n\n"
                "/start - Start the bot\n"
                "/help - Show help\n"
                "/info - Bot information\n"
                "/quote - Random quote\n"
                "/menu - Interactive menu\n"
                "/stats - Your statistics"
            )
        elif callback_data == "info":
            text = (
                f"Bot Name: Simple Telegram Bot\n"
                f"Version: 1.0.0\n"
                f"Total Users: {len(user_data_store)}\n"
                f"Time: {datetime.now().strftime('%H:%M:%S')}"
            )
        elif callback_data == "quote":
            text = f"\"{random.choice(QUOTES)}\""
        elif callback_data == "stats":
            if user_id in user_data_store:
                data = user_data_store[user_id]
                text = (
                    f"Username: @{data.get('username', 'N/A')}\n"
                    f"Messages: {data.get('message_count', 0)}"
                )
            else:
                text = "No data found."
        else:
            text = "Unknown action"

        await query.edit_message_text(text=text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text

        # Update message count
        if user_id in user_data_store:
            user_data_store[user_id]['message_count'] += 1

        # Simple responses based on message content
        response = self._generate_response(message_text)
        await update.message.reply_text(response)

        logger.info(f"Message from {user_id}: {message_text[:50]}...")

    def _generate_response(self, message: str) -> str:
        """Generate a response based on message content"""
        message_lower = message.lower()

        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I help you today?"
        elif any(word in message_lower for word in ['bye', 'goodbye']):
            return "Goodbye! Have a great day!"
        elif any(word in message_lower for word in ['thanks', 'thank you']):
            return "You're welcome!"
        elif '?' in message:
            return "That's an interesting question. Try using /help to see what I can do!"
        else:
            return f"You said: {message}\n\nUse /help to see available commands."

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Error: {context.error}")

        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Sorry, an error occurred. Please try again later."
            )

    def run(self) -> None:
        """Run the bot"""
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found!")
        print("Please create a .env file with your bot token.")
        print("Example: TELEGRAM_BOT_TOKEN=your_token_here")
        return

    try:
        bot = TelegramBot(TOKEN)
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == '__main__':
    main()
