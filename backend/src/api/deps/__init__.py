from typing import Annotated

import fastapi
import pydantic
from fastapi import security, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from api import crud, database, exceptions, models, schemas
from api.settings import _Settings, get_settings

Engine = Annotated[AsyncEngine, fastapi.Depends(database.get_engine)]
SessionFactory = Annotated[
    async_sessionmaker[AsyncSession], fastapi.Depends(database.get_session_factory)
]
Settings = Annotated[_Settings, fastapi.Depends(get_settings)]


oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="v1/auth/token")

AccessToken = Annotated[str, fastapi.Depends(oauth2_scheme)]


UNAUTHORIZED_EXCEPTION = fastapi.HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: AccessToken, session_factory: SessionFactory, settings: Settings
) -> models.User:
    try:
        token_data = schemas.token.TokenData(
            **jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.access_token_sign_algorithm],
            )
        )
        async with session_factory() as db:
            user = await crud.user.get_user_by_username(db, token_data.sub)
    except (JWTError, pydantic.ValidationError, exceptions.UserNotFound) as err:
        raise UNAUTHORIZED_EXCEPTION from err
    return user


CurrentUser = Annotated[models.User, fastapi.Depends(get_current_user)]
