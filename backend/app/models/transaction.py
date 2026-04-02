"""
Transaction model for tracking financial operations.
Supports expenses, income, and transfers between accounts.
"""

from beanie import Document, Link
from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional, Literal
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"


class AccountType(str, Enum):
    """Account type enumeration."""
    CASH = "cash"
    CARD = "card"


class Transaction(Document):
    """
    Transaction document representing a financial operation.
    Can be an expense, income, or transfer between accounts.
    """

    # User reference
    user_id: int = Field(..., description="Telegram user ID")

    # Transaction details
    amount: float = Field(..., gt=0, description="Transaction amount (always positive)")
    type: TransactionType = Field(..., description="Transaction type (expense/income/transfer)")

    # Accounts involved
    source_account: AccountType = Field(..., description="Source account (cash/card)")
    destination_account: Optional[AccountType] = Field(
        default=None,
        description="Destination account (only for transfers)"
    )

    # Categorization
    category_id: Optional[str] = Field(default=None, description="Category ID reference")
    category_name: str = Field(..., description="Category name (denormalized for performance)")

    # Additional info
    note: Optional[str] = Field(default=None, max_length=500, description="Optional note")

    # Dates
    date: datetime = Field(..., description="Transaction date (user can set custom date)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Settings:
        name = "transactions"
        indexes = [
            "user_id",
            "type",
            "date",
            [("user_id", 1), ("date", -1)],  # Composite for user history queries
            [("user_id", 1), ("type", 1)],
            [("user_id", 1), ("category_id", 1)],
        ]

    @field_validator('destination_account')
    @classmethod
    def validate_destination_account(cls, v, info):
        """Validate that destination_account is only set for transfers."""
        transaction_type = info.data.get('type')

        if transaction_type == TransactionType.TRANSFER:
            if v is None:
                raise ValueError("destination_account is required for transfers")
            if v == info.data.get('source_account'):
                raise ValueError("source_account and destination_account must be different")
        else:
            if v is not None:
                raise ValueError("destination_account should only be set for transfers")

        return v

    def __repr__(self):
        return f"<Transaction {self.type.value} {self.amount} from {self.source_account.value}>"

    def __str__(self):
        if self.type == TransactionType.TRANSFER:
            return f"Transfer {self.amount} from {self.source_account.value} to {self.destination_account.value}"
        return f"{self.type.value.capitalize()} {self.amount} ({self.category_name})"

    @property
    def display_amount(self) -> float:
        """
        Return amount with appropriate sign for display.
        Expenses are negative, income and transfers are positive.
        """
        if self.type == TransactionType.EXPENSE:
            return -self.amount
        return self.amount
