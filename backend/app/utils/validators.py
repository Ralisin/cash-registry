"""
Validation utility functions.
"""

from datetime import datetime
from typing import Optional


def validate_amount(amount: float) -> bool:
    """
    Validate that an amount is positive and reasonable.

    Args:
        amount: The amount to validate

    Returns:
        True if valid, False otherwise
    """
    return amount > 0 and amount < 1_000_000_000  # Max 1 billion


def validate_date(date: datetime) -> bool:
    """
    Validate that a date is not in the future and not too far in the past.

    Args:
        date: The date to validate

    Returns:
        True if valid, False otherwise
    """
    now = datetime.utcnow()
    # Not in the future
    if date > now:
        return False
    # Not more than 10 years in the past
    ten_years_ago = now.replace(year=now.year - 10)
    if date < ten_years_ago:
        return False
    return True


def validate_balance_sufficient(current_balance: float, amount: float) -> bool:
    """
    Validate that a balance is sufficient for a transaction.

    Args:
        current_balance: Current account balance
        amount: Transaction amount

    Returns:
        True if sufficient, False otherwise
    """
    return current_balance >= amount


def format_currency(amount: float, currency: str = "EUR") -> str:
    """
    Format an amount as currency string.

    Args:
        amount: Amount to format
        currency: Currency code (EUR, USD, etc.)

    Returns:
        Formatted currency string
    """
    symbols = {
        "EUR": "€",
        "USD": "$",
        "GBP": "£",
        "CHF": "CHF",
    }

    symbol = symbols.get(currency, currency)

    # Format with 2 decimals
    formatted = f"{amount:,.2f}"

    # Symbol placement (EUR after, others before)
    if currency == "EUR":
        return f"{formatted} {symbol}"
    else:
        return f"{symbol} {formatted}"
