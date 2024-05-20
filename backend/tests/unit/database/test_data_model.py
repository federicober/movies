from typing import Any

import sqlmodel
from movies.core.database import data_model

from tests.unit.database.conftest import SqlSessionFactory


def _user_factory(**kwargs: Any) -> data_model.User:
    base_kwargs: dict[str, Any] = dict(
        email="foo@example.org",
        hashed_password="password",
    )
    base_kwargs.update(kwargs)
    base_kwargs.setdefault("display_name", base_kwargs["email"])
    return data_model.User(**base_kwargs)


def test_user_model(sql_session_factory: SqlSessionFactory) -> None:
    with sql_session_factory() as session:
        user = _user_factory()
        print(repr(user))
        session.add(user)

        session.commit()

        selected_user = session.exec(sqlmodel.select(data_model.User)).first()

    assert selected_user is not None

    assert selected_user.id is not None
    assert selected_user.display_name == user.display_name
    assert selected_user.email == user.email
    assert selected_user.hashed_password == user.hashed_password


def test_user_session_link(sql_session_factory: SqlSessionFactory) -> None:
    with sql_session_factory() as session:
        user_1 = _user_factory()
        user_2 = _user_factory(email="bar@example.net")
        user_3 = _user_factory(email="baz@example.com")
        session.add_all([user_1, user_2, user_3])

        session.commit()

        movie_session_1 = data_model.Session(
            reference="foo_session_1", users=[user_1, user_2]
        )
        movie_session_2 = data_model.Session(
            reference="foo_session_1", users=[user_2, user_3]
        )

        session.add_all([movie_session_1, movie_session_2])

        session.commit()

        assert [s.reference for s in user_1.sessions] == [movie_session_1.reference]
        assert [s.reference for s in user_2.sessions] == [
            movie_session_1.reference,
            movie_session_2.reference,
        ]
