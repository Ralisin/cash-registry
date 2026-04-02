"""
Category management API routes.
Handles listing and managing user categories.
"""

from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.category import Category
from app.models.user import User
from app.models.transaction import Transaction
from app.utils.telegram_auth import validate_telegram_init_data, extract_user_from_init_data


router = APIRouter()


# Request/Response models

class CategoryCreateRequest(BaseModel):
    """Request model for creating a custom category."""
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    icon: Optional[str] = Field(None, max_length=10, description="Icon emoji or name")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="Hex color code")


class CategoryUpdateRequest(BaseModel):
    """Request model for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="New category name")
    icon: Optional[str] = Field(None, max_length=10, description="New icon")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="New color")


class CategoryResponse(BaseModel):
    """Response model for category data."""
    id: str
    name: str
    is_default: bool
    user_id: Optional[int]
    icon: Optional[str]
    color: Optional[str]
    created_at: datetime

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


# Endpoints

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """
    Get all categories available to the user.
    Includes default categories and user's custom categories.
    """
    user = await get_user_from_init_data(init_data)

    # Get default categories and user's custom categories
    categories = await Category.find(
        {
            "$or": [
                {"is_default": True},
                {"user_id": user.telegram_id}
            ]
        }
    ).sort("name").to_list()

    return [
        CategoryResponse(
            id=str(c.id),
            name=c.name,
            is_default=c.is_default,
            user_id=c.user_id,
            icon=c.icon,
            color=c.color,
            created_at=c.created_at
        )
        for c in categories
    ]


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    request: CategoryCreateRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Create a custom category."""
    user = await get_user_from_init_data(init_data)

    # Check if category with same name already exists for this user
    existing = await Category.find_one(
        {
            "name": request.name,
            "$or": [
                {"is_default": True},
                {"user_id": user.telegram_id}
            ]
        }
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists"
        )

    # Create category
    category = Category(
        name=request.name,
        is_default=False,
        user_id=user.telegram_id,
        icon=request.icon,
        color=request.color
    )

    await category.insert()

    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        is_default=category.is_default,
        user_id=category.user_id,
        icon=category.icon,
        color=category.color,
        created_at=category.created_at
    )


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Get a specific category by ID."""
    user = await get_user_from_init_data(init_data)

    category = await Category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Verify access (must be default or user's own)
    if not category.is_default and category.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own categories"
        )

    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        is_default=category.is_default,
        user_id=category.user_id,
        icon=category.icon,
        color=category.color,
        created_at=category.created_at
    )


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    request: CategoryUpdateRequest,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """Update a custom category."""
    user = await get_user_from_init_data(init_data)

    category = await Category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Cannot update default categories
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update default categories"
        )

    # Verify ownership
    if category.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own categories"
        )

    # Update fields
    if request.name is not None:
        # Check for name conflicts
        existing = await Category.find_one(
            {
                "name": request.name,
                "_id": {"$ne": category.id},
                "$or": [
                    {"is_default": True},
                    {"user_id": user.telegram_id}
                ]
            }
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A category with this name already exists"
            )

        old_name = category.name
        category.name = request.name

        # Update category_name in all transactions using this category
        transactions = await Transaction.find(Transaction.category_id == category_id).to_list()
        for transaction in transactions:
            transaction.category_name = request.name
            await transaction.save()

    if request.icon is not None:
        category.icon = request.icon

    if request.color is not None:
        category.color = request.color

    await category.save()

    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        is_default=category.is_default,
        user_id=category.user_id,
        icon=category.icon,
        color=category.color,
        created_at=category.created_at
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    replacement_category_id: Optional[str] = None,
    init_data: str = Header(..., alias="X-Telegram-Init-Data")
):
    """
    Delete a custom category.
    If the category is used in transactions, a replacement category must be provided.
    """
    user = await get_user_from_init_data(init_data)

    category = await Category.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Cannot delete default categories
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete default categories"
        )

    # Verify ownership
    if category.user_id != user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own categories"
        )

    # Check if category is used in transactions
    transactions_count = await Transaction.find(Transaction.category_id == category_id).count()

    if transactions_count > 0:
        if not replacement_category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This category is used in {transactions_count} transactions. "
                       "Please provide a replacement_category_id."
            )

        # Validate replacement category
        replacement_category = await Category.get(replacement_category_id)
        if not replacement_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Replacement category not found"
            )

        if not replacement_category.is_default and replacement_category.user_id != user.telegram_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Replacement category must be yours or a default category"
            )

        # Update all transactions with replacement category
        transactions = await Transaction.find(Transaction.category_id == category_id).to_list()
        for transaction in transactions:
            transaction.category_id = replacement_category_id
            transaction.category_name = replacement_category.name
            await transaction.save()

    # Delete category
    await category.delete()

    return None
