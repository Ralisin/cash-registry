"""
Application configuration using Pydantic Settings.
Loads configuration from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # MongoDB Configuration
    mongodb_url: str
    database_name: str = "scout_finance"

    # Telegram Bot Configuration
    telegram_bot_token: str

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 10000
    debug: bool = False

    # Frontend URL for CORS
    frontend_url: str

    # Security
    secret_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
