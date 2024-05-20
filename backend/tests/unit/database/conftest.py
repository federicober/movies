import contextlib
import pathlib
from typing import Callable, ContextManager, Iterator, TypeAlias

import pytest
import sqlalchemy
import sqlmodel
from movies._types import AsyncContextManagerFactory
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture()
def sql_engine(tmp_path: pathlib.Path) -> sqlalchemy.Engine:
    engine = sqlmodel.create_engine(f"sqlite:///{tmp_path}/database.db")
    sqlmodel.SQLModel.metadata.create_all(engine)
    return engine


SqlSessionFactory: TypeAlias = Callable[[], ContextManager[sqlmodel.Session]]


@pytest.fixture()
def sql_session_factory(sql_engine: sqlalchemy.Engine) -> SqlSessionFactory:
    @contextlib.contextmanager
    def sql_session() -> Iterator[sqlmodel.Session]:
        with sqlmodel.Session(sql_engine) as session:
            yield session

    return sql_session


@pytest.fixture()
def sql_async_engine(
    tmp_path: pathlib.Path,
    # use the engine fixture to ensure that the tables are created
    sql_engine: sqlalchemy.Engine,
) -> AsyncEngine:
    return create_async_engine(f"sqlite+aiosqlite:///{tmp_path}/database.db", echo=True)


@pytest.fixture()
def sql_async_session_factory(
    sql_async_engine: AsyncEngine,
) -> AsyncContextManagerFactory[AsyncSession]:
    return async_sessionmaker(sql_async_engine, class_=AsyncSession, autoflush=False)
