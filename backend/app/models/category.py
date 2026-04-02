"""
Category model for transaction categorization.
Includes default scout categories and user-custom categories.
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional


# Default categories for Scout Agesci
DEFAULT_CATEGORIES = [
    "Materiali scout",
    "Affitto sede",
    "Campo/Uscite",
    "Trasporti",
    "Attività",
    "Cibo/Bevande",
    "Assicurazioni/Quote",
    "Uniformi/Fazzolettoni",
    "Altro",
]


class Category(Document):
    """
    Category document for organizing transactions.
    Can be default (system-wide) or user-specific (custom).
    """

    name: str = Field(..., description="Category name")
    is_default: bool = Field(default=False, description="True if system default category")
    user_id: Optional[int] = Field(default=None, description="Telegram user ID (null for default)")

    # Icon/color for UI (optional, can be added later)
    icon: Optional[str] = Field(default=None, description="Icon name or emoji")
    color: Optional[str] = Field(default=None, description="Hex color code")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation date")

    class Settings:
        name = "categories"
        indexes = [
            "user_id",
            "is_default",
            [("user_id", 1), ("name", 1)],  # Composite index for uniqueness
        ]

    def __repr__(self):
        category_type = "default" if self.is_default else f"custom (user {self.user_id})"
        return f"<Category '{self.name}' ({category_type})>"

    def __str__(self):
        return self.name


async def initialize_default_categories():
    """
    Initialize default categories if they don't exist.
    Should be called on application startup.
    """
    existing_defaults = await Category.find(Category.is_default == True).to_list()

    if not existing_defaults:
        print("📦 Initializing default categories...")

        default_categories = [
            Category(name=name, is_default=True, user_id=None)
            for name in DEFAULT_CATEGORIES
        ]

        await Category.insert_many(default_categories)
        print(f"✅ Created {len(default_categories)} default categories")
    else:
        print(f"✅ Found {len(existing_defaults)} existing default categories")
