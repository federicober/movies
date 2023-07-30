from datetime import datetime, timedelta
from typing import Annotated

import fastapi
from fastapi import security
from jose import jwt

from api import crud, deps, schemas

router = fastapi.APIRouter(tags=["auth"])

__all__ = ["router"]


def create_access_token(data: schemas.token.TokenData, settings: deps.Settings) -> str:
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
    session_factory: deps.SessionFactory,
) -> schemas.token.Token:
    async with session_factory() as db:
        user = await crud.user.authenticate_user(
            db, form_data.username, form_data.password
        )
    if not user:
        raise deps.UNAUTHORIZED_EXCEPTION

    access_token = create_access_token(
        schemas.token.TokenData(sub=user.username), settings
    )
    return schemas.token.Token(access_token=access_token)


@router.get("/users/me")
async def read_users_me(current_user: deps.CurrentUser) -> schemas.user.User:
    return schemas.user.User.model_validate(current_user)
