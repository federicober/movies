from typing import Protocol

from movies.core.database import data_model


class IUserRepo(Protocol):
    async def get(self, email: str) -> data_model.User: ...

    async def create(self, display_name: str, email: str, password: str) -> None: ...

    async def authenticate(self, email: str, password: str) -> data_model.User: ...
