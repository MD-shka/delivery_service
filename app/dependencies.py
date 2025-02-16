import uuid
from typing import AsyncGenerator

from fastapi import Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.db import get_session as _get_db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _get_db_session() as session:
        yield session


async def get_session_id(session_id: str | None = Cookie(None)) -> str:
    if session_id is None:
        session_id = str(uuid.uuid4())
    return session_id
