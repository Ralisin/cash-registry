"""
Transaction management API routes.
Handles creation, retrieval, update, and deletion of transactions.
"""

from fastapi import APIRouter, HTTPException, Header, Query, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.models.transaction import Transaction, TransactionType, AccountType
from app.models.user import User
from app.models.category import Category
from app.utils.telegram_auth import validate_telegram_init_data, extract_user_from_init_data
from app.utils.validators import validate_balance_sufficient


router = APIRouter()


# Request/Response models

class TransactionCreateRequest(BaseModel):
    """Request model for creating a transaction."""
    amount: float = Field(..., gt=0, description="Transaction amount")
    type: TransactionType = Field(..., description="Transaction type")
    source_account: AccountType = Field(..., description="Source account")
    category_id: str = Field(..., description="Category ID")
    note: Optional[str] = Field(None, max_length=500, description="Optional note")
    date: Optional[datetime] = Field(None, description="Transaction date (defaults to now)")


class TransferRequest(BaseModel):
    """Request model for transfers between accounts."""
    amount: float = Field(..., gt=0, description="Transfer amount")
    source_account: AccountType = Field(..., description="Source account")
    destination_account: AccountType = Field(..., description="Destination account")
    note: Optional[str] = Field(None, max_length=500, description="Optional note")
    date: Optional[datetime] = Field(None, description="Transfer date (defaults to now)")


class TransactionUpdateRequest(BaseModel):
    """Request model for updating a transaction."""
    amount: Optional[float] = Field(None, gt=0, description="New amount")
    category_id: Optional[str] = Field(None, description="New category ID")
    note: Optional[str] = Field(None, max_length=500, description="New note")
    date: Optional[datetime] = Field(None, description="New date")


class TransactionResponse(BaseModel):
    """Response model for transaction data."""
    id: str
    user_id: int
    amount: float
    type: TransactionType
    source_account: AccountType
    destination_account: Optional[AccountType]
    category_id: Optional[str]
    category_name: str
    note: Optional[str]
    date: datetime
    created_at: datetime
    updated_at: datetime
    display_amount: float

    class Config:
        from_attributes = True


# Helper functions

async def get_user_from_init_data(init_data: str) -> User:
    """Validate initData and get user."""
    if not validate_telegram_init_data(init_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication"
        )

    user_info = extract_user_from_init_data(init_data)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract user info"
        )

    user = await User.find_one(User.telegram_id == user_info['telegram_id'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


async def update_balance_for_transaction(
    user: User,
    transaction_type: TransactionType,
    amount: float,
    source_account: AccountType,
    destination_account: Optional[AccountType] = None
):
    """Update user balance based on transaction."""
    if transaction_type == TransactionType.EXPENSE:
        # Deduct from source account
        if source_account == AccountType.CASH:
            if not validate_balance_sufficient(user.account.cash_balance, amount):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient cash balance"
                )
            user.account.cash_balance -= amount
        else:  # CARD
            if not validate_balance_sufficient(user.account.card_balance, amount):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient card balance"
                )
            user.account.card_balance -= amount

    elif transaction_type == TransactionType.INCOME:
        # Add to source account
        if source_account == AccountType.CASH:
            user.account.cash_balance += amount
        else:  # CARD
            user.account.card_balance += amount

    elif transaction_type == TransactionType.TRANSFER:
        # Transfer from source to destination
        if source_account == AccountType.CASH:
            if not validate_balance_sufficient(user.account.cash_balance, amount):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient cash balance for transfer"
                )
            user.account.cash_balance -= amount
            user.account.card_balance += amount
        else:  # CARD to CASH
            if not validate_balance_sufficient(user.account.card_balance, amount):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient card balance for transfer"
                )
            user.account.card_balance -= amount
            user.account.cash_balance += amount

    await user.save()


async def reverse_transaction_balance(transaction: Transaction, user: User):
    """Reverse the balance changes of a transaction before deletion/update."""
    if transaction.type == TransactionType.EXPENSE:
        # Refund to source account
        if transaction.source_account == AccountType.CASH:
            user.account.cash_balance += transaction.amount
        else:
            user.account.card_balance += transaction.amount

    elif transaction.type == TransactionType.INCOME:
        # Remove from source account
        if transaction.source_account == AccountType.CASH:
            user.account.cash_balance -= transaction.amount
        else:
            user.account.card_balance -= transaction.amount

    elif transaction.type == TransactionType.TRANSFER:
        # Reverse transfer
        if transaction.source_account == AccountType.CASH:
            user.account.cash_balance += transaction.amount
            user.account.card_balance -= transaction.amount
        else:
            user.account.card_balance += transaction.amount
            user.account.cash_balance -= transaction.amount

    await user.save()


# Endpoints

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    request: TransactionCreateRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Create a new transaction (expense or income)."""
    user = await get_user_from_init_data(init_data)

    # Get category
    category = await Category.get(request.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Verify category belongs to user or is default
    if not category.is_default and category.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only use your own categories or default categories"
        )

    # Create transaction
    transaction = Transaction(
        user_id=user.telegram_id,
        amount=request.amount,
        type=request.type,
        source_account=request.source_account,
        category_id=request.category_id,
        category_name=category.name,
        note=request.note,
        date=request.date or datetime.utcnow()
    )

    # Update balance
    await update_balance_for_transaction(
        user,
        request.type,
        request.amount,
        request.source_account
    )

    await transaction.insert()

    return TransactionResponse(
        id=str(transaction.id),
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        category_id=transaction.category_id,
        category_name=transaction.category_name,
        note=transaction.note,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        display_amount=transaction.display_amount
    )


@router.post("/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transfer(
    request: TransferRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Create a transfer between accounts."""
    user = await get_user_from_init_data(init_data)

    # Validate accounts are different
    if request.source_account == request.destination_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination accounts must be different"
        )

    # Create transaction
    transaction = Transaction(
        user_id=user.telegram_id,
        amount=request.amount,
        type=TransactionType.TRANSFER,
        source_account=request.source_account,
        destination_account=request.destination_account,
        category_id=None,
        category_name="Transfer",
        note=request.note,
        date=request.date or datetime.utcnow()
    )

    # Update balance
    await update_balance_for_transaction(
        user,
        TransactionType.TRANSFER,
        request.amount,
        request.source_account,
        request.destination_account
    )

    await transaction.insert()

    return TransactionResponse(
        id=str(transaction.id),
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        category_id=transaction.category_id,
        category_name=transaction.category_name,
        note=transaction.note,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        display_amount=transaction.display_amount
    )


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    init_data: str = Header(..., alias="X-Telegram-Init-Data"),
    type: Optional[TransactionType] = Query(None, description="Filter by type"),
    category_id: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    limit: int = Query(100, ge=1, le=1000, description="Number of results"),
    skip: int = Query(0, ge=0, description="Number of results to skip")
):
    """Get user's transactions with optional filters."""
    user = await get_user_from_init_data(init_data)

    # Build query
    query = {"user_id": user.telegram_id}

    if type:
        query["type"] = type

    if category_id:
        query["category_id"] = category_id

    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = start_date
        if end_date:
            date_query["$lte"] = end_date
        query["date"] = date_query

    # Execute query
    transactions = await Transaction.find(query).sort([("date", -1)]).skip(skip).limit(limit).to_list()

    return [
        TransactionResponse(
            id=str(t.id),
            user_id=t.user_id,
            amount=t.amount,
            type=t.type,
            source_account=t.source_account,
            destination_account=t.destination_account,
            category_id=t.category_id,
            category_name=t.category_name,
            note=t.note,
            date=t.date,
            created_at=t.created_at,
            updated_at=t.updated_at,
            display_amount=t.display_amount
        )
        for t in transactions
    ]


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Get a specific transaction by ID."""
    user = await get_user_from_init_data(init_data)

    transaction = await Transaction.get(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Verify ownership
    if transaction.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own transactions"
        )

    return TransactionResponse(
        id=str(transaction.id),
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        category_id=transaction.category_id,
        category_name=transaction.category_name,
        note=transaction.note,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        display_amount=transaction.display_amount
    )


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    request: TransactionUpdateRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Update a transaction."""
    user = await get_user_from_init_data(init_data)

    transaction = await Transaction.get(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Verify ownership
    if transaction.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own transactions"
        )

    # Cannot update transfers
    if transaction.type == TransactionType.TRANSFER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfers cannot be updated, please delete and create a new one"
        )

    # Reverse old transaction
    await reverse_transaction_balance(transaction, user)

    # Update fields
    if request.amount is not None:
        transaction.amount = request.amount

    if request.category_id is not None:
        category = await Category.get(request.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        if not category.is_default and category.user_id != user.telegram_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only use your own categories"
            )
        transaction.category_id = request.category_id
        transaction.category_name = category.name

    if request.note is not None:
        transaction.note = request.note

    if request.date is not None:
        transaction.date = request.date

    transaction.updated_at = datetime.utcnow()

    # Apply new transaction
    await update_balance_for_transaction(
        user,
        transaction.type,
        transaction.amount,
        transaction.source_account
    )

    await transaction.save()

    return TransactionResponse(
        id=str(transaction.id),
        user_id=transaction.user_id,
        amount=transaction.amount,
        type=transaction.type,
        source_account=transaction.source_account,
        destination_account=transaction.destination_account,
        category_id=transaction.category_id,
        category_name=transaction.category_name,
        note=transaction.note,
        date=transaction.date,
        created_at=transaction.created_at,
        updated_at=transaction.updated_at,
        display_amount=transaction.display_amount
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Delete a transaction."""
    user = await get_user_from_init_data(init_data)

    transaction = await Transaction.get(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Verify ownership
    if transaction.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own transactions"
        )

    # Reverse transaction balance
    await reverse_transaction_balance(transaction, user)

    # Delete transaction
    await transaction.delete()

    return None
