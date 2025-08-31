from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

_engine = None
_Session: async_sessionmaker[AsyncSession] | None = None


def get_engine():
    global _engine
    if _engine is None:
        if not settings.DATABASE_URL:
            raise RuntimeError("DATABASE_URL не настроен")
        _engine = create_async_engine(
            settings.DATABASE_URL, future=True, echo=False, pool_pre_ping=True
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _Session
    if _Session is None:
        _Session = async_sessionmaker(
            get_engine(), expire_on_commit=False, autoflush=False, autocommit=False
        )
    return _Session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        await session.close()
