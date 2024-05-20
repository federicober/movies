from typing import AsyncIterator

import pytest
from movies._types import AsyncContextManagerFactory
from movies.core import exceptions
from movies.core.repositories.user_repo import UserRepo
from sqlmodel.ext.asyncio.session import AsyncSession

pytestmark = pytest.mark.anyio


@pytest.fixture()
async def user_repo(
    sql_async_session_factory: AsyncContextManagerFactory[AsyncSession],
) -> AsyncIterator[UserRepo]:
    async with sql_async_session_factory() as session:
        yield UserRepo(session)


async def test_user_repo_create_get_returns_same_user(user_repo: UserRepo) -> None:
    email = "foo@example.org"
    display_name = "foo_user"

    await user_repo.create(display_name, email, "foo_password")
    await user_repo.db_session.commit()

    user = await user_repo.get(email)

    assert user.display_name == display_name
    assert user.email == email
    assert not hasattr(user, "password")


async def test_user_repo_raises_conflict_if_user_already_exists(
    user_repo: UserRepo,
) -> None:
    email = "foo@example.org"

    await user_repo.create("foo_user", email, "foo_password")
    await user_repo.db_session.commit()

    with pytest.raises(exceptions.UserAlreadyExists):
        await user_repo.create("Foo User", email, "foo password 2")


async def test_user_repo_create_authenticate_returns_same_user(
    user_repo: UserRepo,
) -> None:
    email = "foo@example.org"
    display_name = "foo_user"
    password = "foo_password"

    await user_repo.create(display_name, email, password)
    await user_repo.db_session.commit()

    user = await user_repo.authenticate(email, password)

    assert user.display_name == display_name
    assert user.email == email
    assert not hasattr(user, "password")


async def test_user_repo_raises_exception_when_user_is_not_found(
    user_repo: UserRepo,
) -> None:
    email = "foo@example.org"

    with pytest.raises(exceptions.UserNotFound):
        await user_repo.get(email)


async def test_user_repo_raises_exception_when_bad_authenticated_user(
    user_repo: UserRepo,
) -> None:
    email = "foo@example.org"
    display_name = "foo_user"
    password = "foo_password"

    await user_repo.create(display_name, email, password)
    await user_repo.db_session.commit()

    with pytest.raises(exceptions.IncorrectUserOrPassword):
        await user_repo.authenticate(email, "other_password")


async def test_user_repo_raises_exception_when_authenticating_user_not_exists(
    user_repo: UserRepo,
) -> None:
    email = "foo@example.org"

    with pytest.raises(exceptions.IncorrectUserOrPassword):
        await user_repo.authenticate(email, "other_password")
