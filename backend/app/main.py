"""
Scout Finance App - FastAPI Backend
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.models.category import initialize_default_categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting Scout Finance API...")
    await connect_to_mongo()
    await initialize_default_categories()
    print("✅ Application started successfully")

    yield

    # Shutdown
    print("🛑 Shutting down Scout Finance API...")
    await close_mongo_connection()
    print("✅ Application shut down successfully")


# Create FastAPI application
app = FastAPI(
    title="Scout Finance API",
    description="Personal finance management system for Scout Agesci groups",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
# Allow frontend URLs including Vercel preview deployments
allowed_origins = [
    "http://localhost:5173",
    "https://scout-finance.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow all Vercel preview URLs (scout-finance-*.vercel.app)
    allow_origin_regex=r'https://scout-finance-.*\.vercel\.app'
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "status": "ok",
        "message": "Scout Finance API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "database": "connected"
    }


# Register routers
from app.routes import users, transactions, categories

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Additional routers (will be added in next sprints)
# from app.routes import export
# app.include_router(export.router, prefix="/export", tags=["Export"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
