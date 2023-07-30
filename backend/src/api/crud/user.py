from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import exceptions, models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db: AsyncSession, user_id: int) -> models.User:
    user = await db.scalar(select(models.User).where(models.User.id == user_id))
    if user is None:
        raise exceptions.UserNotFound(user_id)
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    user = await db.scalar(select(models.User).where(models.User.username == username))
    if user is None:
        raise exceptions.UserNotFound(username)
    return user


async def create_user(db: AsyncSession, user: schemas.user.CreateUser) -> None:
    hashed_password = _get_password_hash(user.password)
    db.add(models.User(username=user.username, password=hashed_password))


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> models.User | None:
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not _verify_password(password, user.password):
        return None
    return user
