"""
Database configuration and setup
यहाँ database से connect करते हैं
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Database URL से connect करना
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://intelliflow_user:intelliflow_password_123@localhost:5432/intelliflow_db"
)

# Async URL (PostgreSQL के लिए asyncpg driver)
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Database engine बनाएं
# Echo=true = SQL queries को console में दिखाएगा
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true",
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    poolclass=NullPool
)

# Session बनाने का factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base class सभी models के लिए
Base = declarative_base()

# FastAPI में हर endpoint को database session देने के लिए
async def get_db() -> AsyncSession:
    """
    Dependency: FastAPI को हर request में database session देगा
    
    Usage:
    @app.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        # अब db use कर सकते हो
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()

# पहली बार जब app start हो तो tables बनाएं
async def init_db():
    """
    सभी tables create करें (अगर पहले से न हों)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created/verified")

async def close_db():
    """
    App shutdown के समय database connection बंद करें
    """
    await engine.dispose()
    logger.info("Database connection closed")
