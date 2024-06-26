from typing import Annotated, cast

import fastapi
import jwt
import pydantic
from fastapi import security, status

from movies._types import AsyncContextManagerFactory
from movies.api import config, schemas, state
from movies.core import exceptions, transaction
from movies.core.database import data_model

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="v1/auth/token")

AccessToken = Annotated[str, fastapi.Depends(oauth2_scheme)]


UNAUTHORIZED_EXCEPTION = fastapi.HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_app_state(request: fastapi.requests.HTTPConnection) -> state.AppState:
    return cast(state.AppState, request.state._state)


AppState = Annotated[state.AppState, fastapi.Depends(get_app_state)]


async def get_settings(state: AppState) -> config.Settings:
    return state["settings"]


Settings = Annotated[config.Settings, fastapi.Depends(get_settings)]


async def get_transaction_factory(
    state: AppState,
) -> AsyncContextManagerFactory[transaction.ITransaction]:
    return state["transaction_factory"]


TransactionFactory = Annotated[
    AsyncContextManagerFactory[transaction.ITransaction],
    fastapi.Depends(get_transaction_factory),
]


async def get_current_user(
    token: AccessToken, settings: Settings, transaction_factory: TransactionFactory
) -> data_model.User:
    try:
        token_data = schemas.token.TokenData(
            **jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.access_token_sign_algorithm],
            )
        )
    except (jwt.PyJWTError, pydantic.ValidationError, exceptions.UserNotFound) as err:
        raise UNAUTHORIZED_EXCEPTION from err
    async with transaction_factory() as transaction:
        user = await transaction.users.get(token_data.sub)
    return user


CurrentUser = Annotated[data_model.User, fastapi.Depends(get_current_user)]
