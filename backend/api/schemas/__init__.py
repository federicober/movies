from typing import Literal
import pydantic


class Session(pydantic.BaseModel):
    id: str


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
