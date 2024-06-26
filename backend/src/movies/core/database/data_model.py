from typing import Optional

import sqlmodel


class UserSessionLink(sqlmodel.SQLModel, table=True):
    user_id: Optional[int] = sqlmodel.Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    session_id: Optional[int] = sqlmodel.Field(
        default=None, foreign_key="session.id", primary_key=True
    )


class User(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    display_name: str
    email: str = sqlmodel.Field(unique=True, index=True)
    hashed_password: str

    sessions: list["Session"] = sqlmodel.Relationship(
        back_populates="users",
        link_model=UserSessionLink,
    )


class Session(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    reference: str

    users: list["User"] = sqlmodel.Relationship(
        back_populates="sessions", link_model=UserSessionLink
    )


class Movie(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    reference: str = sqlmodel.Field(unique=True, index=True)
    title: str
    image_url: str
