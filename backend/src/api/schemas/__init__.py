from typing import Literal

import pydantic

from . import _token as token
from . import _user as user


class Session(pydantic.BaseModel):
    id: str
    members: list[user.User]


class Sessions(pydantic.RootModel[Session]):
    pass


class Movie(pydantic.BaseModel):
    id: str
    title: str
    image_url: str


class Vote(pydantic.BaseModel):
    movie_id: str
    vote: Literal["yes", "no"]


class SessionMatches(pydantic.BaseModel):
    count: int
    movies: list[Movie]
