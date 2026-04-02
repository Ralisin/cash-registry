"""
Database configuration and initialization.
Handles MongoDB connection using Motor and Beanie ODM.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings


# Database client instance
db_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """
    Initialize MongoDB connection and Beanie ODM.
    Called on application startup.
    """
    global db_client

    # Import models here to avoid circular imports
    from app.models.user import User
    from app.models.category import Category
    from app.models.transaction import Transaction

    # Create MongoDB client
    db_client = AsyncIOMotorClient(settings.mongodb_url)

    # Initialize Beanie with document models
    await init_beanie(
        database=db_client[settings.database_name],
        document_models=[User, Category, Transaction]
    )

    print(f"✅ Connected to MongoDB: {settings.database_name}")


async def close_mongo_connection():
    """
    Close MongoDB connection.
    Called on application shutdown.
    """
    global db_client
    if db_client:
        db_client.close()
        print("❌ MongoDB connection closed")


async def get_database():
    """Get database instance."""
    return db_client[settings.database_name]
