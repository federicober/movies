from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from . import settings

__engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global __engine
    if __engine is None:
        settings_ = settings.get_settings()
        __engine = create_async_engine(settings_.db_dsn, echo=True)
    return __engine


__session_factory: async_sessionmaker[AsyncSession] | None = None


async def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global __session_factory
    if __session_factory is None:
        __session_factory = async_sessionmaker(get_engine(), class_=AsyncSession)
    return __session_factory
