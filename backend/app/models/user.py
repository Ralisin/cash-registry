"""
User model for Scout Finance App.
Each user is identified by their Telegram ID.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserSettings(BaseModel):
    """User preferences and settings."""

    currency: str = Field(default="EUR", description="Preferred currency (EUR, USD, GBP, CHF)")
    language: str = Field(default="it", description="Language code (it, en)")
    dark_mode: Optional[bool] = Field(default=None, description="Dark mode preference (None = auto)")


class Account(BaseModel):
    """User's financial accounts (embedded in User)."""

    cash_balance: float = Field(default=0.0, description="Cash balance")
    card_balance: float = Field(default=0.0, description="Card/Bank balance")
    initial_cash: float = Field(default=0.0, description="Initial cash balance (for tracking)")
    initial_card: float = Field(default=0.0, description="Initial card balance (for tracking)")

    @property
    def total_balance(self) -> float:
        """Calculate total balance (cash + card)."""
        return self.cash_balance + self.card_balance

    @property
    def initial_total(self) -> float:
        """Calculate initial total balance."""
        return self.initial_cash + self.initial_card


class User(Document):
    """
    User document representing a Scout Finance App user.
    Identified by Telegram ID.
    """

    telegram_id: int = Field(..., unique=True, description="Telegram user ID")
    name: str = Field(..., description="User's name from Telegram")
    username: Optional[str] = Field(default=None, description="Telegram username")

    # Financial accounts (embedded)
    account: Account = Field(default_factory=Account, description="User's financial accounts")

    # Settings
    settings: UserSettings = Field(default_factory=UserSettings, description="User preferences")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Registration date")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update")

    class Settings:
        name = "users"
        indexes = [
            "telegram_id",
        ]

    def __repr__(self):
        return f"<User {self.telegram_id}: {self.name}>"

    def __str__(self):
        return self.name
