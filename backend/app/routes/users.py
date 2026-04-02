"""
User management API routes.
Handles user registration, profile, settings, and balance management.
"""

from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.user import User, UserSettings, Account
from app.utils.telegram_auth import (
    validate_telegram_init_data,
    extract_user_from_init_data,
    get_user_display_name
)


router = APIRouter()


# Request/Response models
class UserCreateRequest(BaseModel):
    """Request model for user creation."""
    init_data: str = Field(..., description="Telegram Web App initData")


class UserResponse(BaseModel):
    """Response model for user data."""
    telegram_id: int
    name: str
    username: Optional[str]
    account: Account
    settings: UserSettings
    created_at: datetime
    updated_at: datetime


class InitializeBalanceRequest(BaseModel):
    """Request model for initializing balance."""
    cash_balance: float = Field(..., ge=0, description="Initial cash balance")
    card_balance: float = Field(..., ge=0, description="Initial card balance")


class UpdateBalanceRequest(BaseModel):
    """Request model for updating balance."""
    cash_balance: Optional[float] = Field(None, ge=0, description="New cash balance")
    card_balance: Optional[float] = Field(None, ge=0, description="New card balance")


class UpdateSettingsRequest(BaseModel):
    """Request model for updating user settings."""
    currency: Optional[str] = Field(None, pattern="^(EUR|USD|GBP|CHF)$")
    language: Optional[str] = Field(None, pattern="^(it|en)$")
    dark_mode: Optional[bool] = None


class BalanceResponse(BaseModel):
    """Response model for balance data."""
    cash_balance: float
    card_balance: float
    total_balance: float
    initial_cash: float
    initial_card: float
    initial_total: float


# Helper function to get user from initData
async def get_user_from_init_data(init_data: str) -> User:
    """
    Validate initData and get user from database.
    Raises HTTPException if invalid or user not found.
    """
    if not validate_telegram_init_data(init_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication"
        )

    user_info = extract_user_from_init_data(init_data)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract user info from initData"
        )

    user = await User.find_one(User.telegram_id == user_info['telegram_id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register first."
        )

    return user


# Endpoints

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateRequest):
    """
    Register a new user.
    Validates Telegram initData and creates user account.
    """
    # Validate initData
    if not validate_telegram_init_data(request.init_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication"
        )

    # Extract user info
    user_info = extract_user_from_init_data(request.init_data)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract user info from initData"
        )

    # Check if user already exists
    existing_user = await User.find_one(User.telegram_id == user_info['telegram_id'])
    if existing_user:
        # Return existing user
        return existing_user

    # Create new user
    display_name = get_user_display_name(user_info)

    user = User(
        telegram_id=user_info['telegram_id'],
        name=display_name,
        username=user_info.get('username'),
        settings=UserSettings(
            language=user_info.get('language_code', 'it')
        )
    )

    await user.insert()

    return user


@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user(telegram_id: int):
    """Get user by Telegram ID."""
    user = await User.find_one(User.telegram_id == telegram_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch("/{telegram_id}/settings", response_model=UserResponse)
async def update_user_settings(
    telegram_id: int,
    request: UpdateSettingsRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Update user settings."""
    user = await get_user_from_init_data(init_data)

    # Verify user is updating their own settings
    if user.telegram_id != telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own settings"
        )

    # Update settings
    if request.currency is not None:
        user.settings.currency = request.currency
    if request.language is not None:
        user.settings.language = request.language
    if request.dark_mode is not None:
        user.settings.dark_mode = request.dark_mode

    user.updated_at = datetime.utcnow()
    await user.save()

    return user


@router.get("/{telegram_id}/balance", response_model=BalanceResponse)
async def get_balance(telegram_id: int):
    """Get user's balance information."""
    user = await User.find_one(User.telegram_id == telegram_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return BalanceResponse(
        cash_balance=user.account.cash_balance,
        card_balance=user.account.card_balance,
        total_balance=user.account.total_balance,
        initial_cash=user.account.initial_cash,
        initial_card=user.account.initial_card,
        initial_total=user.account.initial_total
    )


@router.post("/{telegram_id}/balance/initialize", response_model=BalanceResponse)
async def initialize_balance(
    telegram_id: int,
    request: InitializeBalanceRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """
    Initialize user's balance.
    Sets both current and initial balance values.
    """
    user = await get_user_from_init_data(init_data)

    # Verify user is updating their own balance
    if user.telegram_id != telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own balance"
        )

    # Set balances
    user.account.cash_balance = request.cash_balance
    user.account.card_balance = request.card_balance
    user.account.initial_cash = request.cash_balance
    user.account.initial_card = request.card_balance

    user.updated_at = datetime.utcnow()
    await user.save()

    return BalanceResponse(
        cash_balance=user.account.cash_balance,
        card_balance=user.account.card_balance,
        total_balance=user.account.total_balance,
        initial_cash=user.account.initial_cash,
        initial_card=user.account.initial_card,
        initial_total=user.account.initial_total
    )


@router.patch("/{telegram_id}/balance", response_model=BalanceResponse)
async def update_balance(
    telegram_id: int,
    request: UpdateBalanceRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """
    Update user's initial balance values.
    This is for correcting the initial balance, not for transactions.
    """
    user = await get_user_from_init_data(init_data)

    # Verify user is updating their own balance
    if user.telegram_id != telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own balance"
        )

    # Update initial balances if provided
    if request.cash_balance is not None:
        # Calculate difference
        diff = request.cash_balance - user.account.initial_cash
        # Apply to both current and initial
        user.account.cash_balance += diff
        user.account.initial_cash = request.cash_balance

    if request.card_balance is not None:
        # Calculate difference
        diff = request.card_balance - user.account.initial_card
        # Apply to both current and initial
        user.account.card_balance += diff
        user.account.initial_card = request.card_balance

    user.updated_at = datetime.utcnow()
    await user.save()

    return BalanceResponse(
        cash_balance=user.account.cash_balance,
        card_balance=user.account.card_balance,
        total_balance=user.account.total_balance,
        initial_cash=user.account.initial_cash,
        initial_card=user.account.initial_card,
        initial_total=user.account.initial_total
    )
