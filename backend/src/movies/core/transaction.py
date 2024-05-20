import contextlib
import dataclasses
from typing import AsyncIterator, Protocol

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from movies.core.repositories.interfaces import IUserRepo
from movies.core.repositories.user_repo import UserRepo


class ITransaction(Protocol):
    @property
    def users(self) -> IUserRepo: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


@dataclasses.dataclass(slots=True, frozen=True)
class Transaction(ITransaction):
    db_session: AsyncSession

    async def commit(self) -> None:
        await self.db_session.commit()

    async def rollback(self) -> None:
        await self.db_session.rollback()

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.db_session)


class TransactionFactory:
    def __init__(self, db_dsn: str) -> None:
        self._db_engine = create_async_engine(db_dsn)
        self._session_maker = async_sessionmaker(self._db_engine, class_=AsyncSession)

    @contextlib.asynccontextmanager
    async def __call__(self) -> AsyncIterator[Transaction]:
        async with self._session_maker() as db_session:
            transaction = Transaction(db_session)
            try:
                yield transaction
            except:
                await transaction.rollback()
