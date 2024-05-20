from typing import TypedDict

from movies._types import AsyncContextManagerFactory
from movies.api.settings import Settings
from movies.core import transaction


class AppState(TypedDict):
    transaction_factory: AsyncContextManagerFactory[transaction.ITransaction]
    settings: Settings
