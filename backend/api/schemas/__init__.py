from typing import Iterator, Literal

import pydantic


class User(pydantic.BaseModel):
    id: str
    name: str
    email: pydantic.EmailStr


class Session(pydantic.BaseModel):
    id: str
    members: list[User]


class Sessions(pydantic.RootModel):
    root: list[Session]

    def __iter__(self) -> Iterator[Session]:
        return iter(self.root)

    def __getitem__(self, item: int) -> Session:
        return self.root[item]


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
