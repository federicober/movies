from datetime import datetime, timedelta, timezone
from typing import Annotated

import fastapi
import jwt
import pydantic
from fastapi import security

from movies.api import deps, schemas
from movies.core import exceptions
from movies.core.database import data_model

router = fastapi.APIRouter(tags=["auth"])


class _Token(pydantic.BaseModel):
    access_token: str
    token_type: str = "Bearer"


class _TokenData(pydantic.BaseModel):
    sub: str


def create_access_token(data: _TokenData, settings: deps.Settings) -> str:
    to_encode = data.model_dump(mode="json")
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.access_token_sign_algorithm
    )
    return encoded_jwt


_OAUTH_PASSWORD_FORM = Annotated[
    security.OAuth2PasswordRequestForm,
    fastapi.Depends(security.OAuth2PasswordRequestForm),
]


@router.post("/token")
async def login_for_access_token(
    form_data: _OAUTH_PASSWORD_FORM,
    settings: deps.Settings,
    transaction_factory: deps.TransactionFactory,
) -> _Token:
    async with transaction_factory() as transaction:
        try:
            user = await transaction.users.authenticate(
                form_data.username, form_data.password
            )
        except exceptions.IncorrectUserOrPassword:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate username or password",
            ) from None

    access_token = create_access_token(_TokenData(sub=user.email), settings)
    return _Token(access_token=access_token)


@router.get("/users/me", response_model=schemas.user.GetUserResponse)
async def read_users_me(current_user: deps.CurrentUser) -> data_model.User:
    return current_user
