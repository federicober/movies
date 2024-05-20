import dataclasses

import sqlalchemy.exc
from passlib.context import CryptContext
from sqlalchemy import insert
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from movies.core import exceptions
from movies.core.database.data_model import User
from movies.core.repositories import interfaces

_PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return _PWD_CONTEXT.verify(plain_password, hashed_password)


def _get_password_hash(password: str) -> str:
    return _PWD_CONTEXT.hash(password)


@dataclasses.dataclass(frozen=True, slots=True)
class UserRepo(interfaces.IUserRepo):
    db_session: AsyncSession

    async def get(self, email: str) -> User:
        user = await self.db_session.scalar(select(User).filter_by(email=email))
        if user is None:
            raise exceptions.UserNotFound()
        return user

    async def create(self, display_name: str, email: str, password: str) -> None:
        hashed_password = _get_password_hash(password)
        try:
            await self.db_session.execute(
                insert(User).values(
                    display_name=display_name,
                    email=email,
                    hashed_password=hashed_password,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            raise exceptions.UserAlreadyExists() from None

    async def authenticate(self, email: str, password: str) -> User:
        try:
            user = await self.get(email)
        except exceptions.UserNotFound:
            raise exceptions.IncorrectUserOrPassword() from None
        if not _verify_password(password, user.hashed_password):
            raise exceptions.IncorrectUserOrPassword()
        return user
