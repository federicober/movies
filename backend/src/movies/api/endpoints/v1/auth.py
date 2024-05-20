from datetime import datetime, timedelta
from typing import Annotated

import fastapi
import pydantic
from fastapi import security
from jose import jwt

from movies.api import deps, schemas
from movies.core.database import data_model

router = fastapi.APIRouter(tags=["auth"])

__all__ = ["router"]


class _Token(pydantic.BaseModel):
    access_token: str
    token_type: str = "Bearer"


class _TokenData(pydantic.BaseModel):
    sub: str


def create_access_token(data: _TokenData, settings: deps.Settings) -> str:
    to_encode = data.model_dump(mode="json")
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
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
    user_repo_factory: deps.UserRepoFactory,
) -> _Token:
    async with user_repo_factory() as user_repo:
        user = await user_repo.authenticate(form_data.username, form_data.password)
    if not user:
        raise deps.UNAUTHORIZED_EXCEPTION

    access_token = create_access_token(_TokenData(sub=user.email), settings)
    return _Token(access_token=access_token)


@router.get("/users/me", response_model=schemas.user.GetUserResponse)
async def read_users_me(current_user: deps.CurrentUser) -> data_model.User:
    return current_user
