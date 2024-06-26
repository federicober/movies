import contextlib
import time
from typing import AsyncIterator, Iterator
from unittest import mock

import fastapi
import freezegun
import jwt
import pytest
from fastapi import testclient
from movies.api import config as settings_module
from movies.api import state
from movies.api.app import app_factory
from movies.core import exceptions
from movies.core.database.data_model import User
from movies.core.repositories.interfaces import IUserRepo
from movies.core.transaction import ITransaction

pytestmark = pytest.mark.anyio


class MockUserRepo(IUserRepo):
    def __init__(self) -> None:
        self._users: dict[str, tuple[User, str]] = {}

    async def create(self, display_name: str, email: str, password: str) -> None:
        if email in self._users:
            raise exceptions.UserAlreadyExists()

        self._users[email] = (
            User(display_name=display_name, email=email, hashed_password="fake_pass"),
            password,
        )

    async def authenticate(self, email: str, password: str) -> User:
        try:
            user, stored_password = self._users[email]
        except KeyError:
            raise exceptions.IncorrectUserOrPassword() from None
        if password != stored_password:
            raise exceptions.IncorrectUserOrPassword()
        return user

    async def get(self, email: str) -> User:
        try:
            user, _ = self._users[email]
        except KeyError:
            raise exceptions.UserNotFound() from None
        return user


class MockTransaction(ITransaction):
    def __init__(self, user_repo: MockUserRepo) -> None:
        self._rollbacked = False
        self._commited = False
        self.user_repo = user_repo

    @property
    def users(self) -> MockUserRepo:
        return self.user_repo

    async def commit(self) -> None:
        self._commited = True

    async def rollback(self) -> None:
        self._rollbacked = True


@pytest.fixture()
def user_repo() -> MockUserRepo:
    return MockUserRepo()


@pytest.fixture()
def secret_key() -> str:
    return "my super secret key"


@pytest.fixture()
def settings(
    secret_key: str, monkeypatch: pytest.MonkeyPatch
) -> settings_module.Settings:
    settings = settings_module.Settings(
        cors_regex=".*", db_dsn="foo.db", secret_key=secret_key
    )
    return settings


@pytest.fixture()
def app(user_repo: MockUserRepo, settings: settings_module.Settings) -> fastapi.FastAPI:
    @contextlib.asynccontextmanager
    async def mock_transaction_factory() -> AsyncIterator[MockTransaction]:
        yield MockTransaction(user_repo)

    @contextlib.asynccontextmanager
    async def mock_lifespan(app: fastapi.FastAPI) -> AsyncIterator[state.AppState]:
        yield {"transaction_factory": mock_transaction_factory, "settings": settings}

    app_ = app_factory(settings)
    app_.router.lifespan_context = mock_lifespan
    return app_


@pytest.fixture()
def test_client(app: fastapi.FastAPI) -> Iterator[testclient.TestClient]:
    with testclient.TestClient(app) as client:
        yield client


def test_get_token_returns_401_when_user_does_not_exist(
    test_client: testclient.TestClient,
) -> None:
    response = test_client.post(
        "/v1/auth/token",
        data={"username": "i_dont_exist@example.org", "password": "some password"},
    )
    assert response.status_code == 401


@freezegun.freeze_time("2024-01-01")
async def test_get_token_returns_access_token_when_valid_auth(
    test_client: testclient.TestClient,
    user_repo: MockUserRepo,
    settings: settings_module.Settings,
) -> None:
    email = "foo_@example.org"
    password = "foo password"
    await user_repo.create("Foo User", email, password)

    response = test_client.post(
        "/v1/auth/token", data={"username": email, "password": password}
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "Bearer"
    decoded = jwt.decode(
        payload["access_token"],
        settings.secret_key,
        algorithms=[settings.access_token_sign_algorithm],
    )
    assert decoded["sub"] == email
    assert decoded["exp"] == time.time() + settings.access_token_expire_minutes * 60
