import logging
from sqlmodel import SQLModel, create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

load_dotenv()

class DatabaseConfig:
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    port: str = os.getenv("DB_PORT")
    host: str = os.getenv("DB_HOST", "localhost")
    database: str = os.getenv("DB_NAME")
    
    @classmethod
    def validate_config(cls) -> bool:
        required_vars = ["DB_USER", "DB_PASSWORD", "DB_PORT", "DB_NAME"]
        return all(os.getenv(var) for var in required_vars)

    @property
    def base_url(self) -> str:
        return f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}/"
    
    @property
    def database_url(self) -> str:
        return f"{self.base_url}{self.database}"

db_config = DatabaseConfig()
if not db_config.validate_config():
    raise ValueError("Missing required database environment variables")

engine = create_async_engine(
    db_config.base_url,
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db() -> None:
    """Initialize the database and create all tables."""
    try:
        async with engine.begin() as conn:
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_config.database}`;"))
            logging.info("MySQL Database Created/Detected.")

        engine_with_db = create_async_engine(
            db_config.database_url,
            echo=True,
            future=True,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        async with engine_with_db.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logging.info("MySQL Database Tables Created.")
            
    except SQLAlchemyError as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    session: Optional[AsyncSession] = None
    try:
        session = async_session_factory()
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Session error: {str(e)}")
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            await session.close()

async def example_usage():
    async with get_session() as session:
        async with session.begin():
            pass