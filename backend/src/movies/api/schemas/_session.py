from typing import Literal

import pydantic

from . import _movie as movie
from . import _user as user


class Session(pydantic.BaseModel):
    reference: str
    members: list[user.BaseUser]


class Sessions(pydantic.RootModel[Session]):
    pass


class Vote(pydantic.BaseModel):
    movie_id: str
    vote: Literal["yes", "no"]


class SessionMatches(pydantic.BaseModel):
    count: int
    movies: list[movie.Movie]
