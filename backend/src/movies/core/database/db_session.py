import functools
from typing import TypeAlias

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from movies import settings


@functools.lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    settings_ = settings.get_settings()
    return create_async_engine(settings_.db_dsn, echo=True)


AsyncSessionFactory: TypeAlias = async_sessionmaker[AsyncSession]


@functools.lru_cache(maxsize=1)
def get_session_factory() -> AsyncSessionFactory:
    return async_sessionmaker(get_engine(), class_=AsyncSession)
