"""
Configuration settings for the Telegram Bot
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    """Bot configuration settings"""

    # Telegram Bot Token (required)
    token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')

    # Bot settings
    bot_name: str = os.getenv('BOT_NAME', 'Simple Telegram Bot')
    bot_version: str = '1.0.0'

    # Admin settings
    admin_ids: list = None

    # Logging
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', 'bot.log')

    # Rate limiting
    rate_limit_messages: int = int(os.getenv('RATE_LIMIT_MESSAGES', '30'))
    rate_limit_period: int = int(os.getenv('RATE_LIMIT_PERIOD', '60'))

    def __post_init__(self):
        """Initialize computed fields"""
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if admin_ids_str:
            self.admin_ids = [int(id.strip()) for id in admin_ids_str.split(',')]
        else:
            self.admin_ids = []

    def validate(self) -> bool:
        """Validate configuration"""
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return True


@dataclass
class DatabaseConfig:
    """Database configuration (optional, for future use)"""

    db_type: str = os.getenv('DB_TYPE', 'sqlite')
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = int(os.getenv('DB_PORT', '5432'))
    db_name: str = os.getenv('DB_NAME', 'telegram_bot')
    db_user: str = os.getenv('DB_USER', '')
    db_password: str = os.getenv('DB_PASSWORD', '')

    @property
    def connection_string(self) -> str:
        """Generate database connection string"""
        if self.db_type == 'sqlite':
            return f"sqlite:///{self.db_name}.db"
        elif self.db_type == 'postgresql':
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif self.db_type == 'mysql':
            return f"mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return ""


# Create default instances
config = BotConfig()
db_config = DatabaseConfig()
