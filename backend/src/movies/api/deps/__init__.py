import contextlib
from typing import Annotated, AsyncIterator

import fastapi
import pydantic
from fastapi import security, status
from jose import JWTError, jwt

from movies._types import AsyncContextManagerFactory
from movies.api import schemas
from movies.core import exceptions
from movies.core.database import AsyncSessionFactory, data_model, get_session_factory
from movies.core.repositories import interfaces
from movies.core.repositories.user_repo import UserRepo
from movies.settings import _Settings, get_settings

SessionFactory = Annotated[AsyncSessionFactory, fastapi.Depends(get_session_factory)]
Settings = Annotated[_Settings, fastapi.Depends(get_settings)]


oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="v1/auth/token")

AccessToken = Annotated[str, fastapi.Depends(oauth2_scheme)]


UNAUTHORIZED_EXCEPTION = fastapi.HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_user_repo_factory(
    session_factory: SessionFactory,
) -> AsyncContextManagerFactory[UserRepo]:
    @contextlib.asynccontextmanager
    async def user_repo() -> AsyncIterator[UserRepo]:
        async with session_factory() as session:
            yield UserRepo(session)

    return user_repo


UserRepoFactory = Annotated[
    AsyncContextManagerFactory[interfaces.IUserRepo],
    fastapi.Depends(get_user_repo_factory),
]


async def get_current_user(
    token: AccessToken, settings: Settings, user_repo_factory: UserRepoFactory
) -> data_model.User:
    try:
        token_data = schemas.token.TokenData(
            **jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.access_token_sign_algorithm],
            )
        )
        async with user_repo_factory() as user_repo:
            user = await user_repo.get(token_data.sub)
    except (JWTError, pydantic.ValidationError, exceptions.UserNotFound) as err:
        raise UNAUTHORIZED_EXCEPTION from err
    return user


CurrentUser = Annotated[data_model.User, fastapi.Depends(get_current_user)]
