from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import db_settings

DATABASE_URL = db_settings.DATABASE_URL

db_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
