from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import db_settings

DATABASE_URL = db_settings.DATABASE_URL

db_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)


def get_session() -> AsyncSession:
    return AsyncSessionLocal()
