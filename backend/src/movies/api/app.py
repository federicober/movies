import contextlib
from typing import AsyncIterator

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from movies.api import config, endpoints, state
from movies.core import transaction


def app_factory(settings_: config.Settings | None = None) -> fastapi.FastAPI:
    if settings_ is None:  # pragma: nocover
        settings_ = config.Settings()  # pyright: ignore[reportCallIssue]

    @contextlib.asynccontextmanager
    async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[state.AppState]:
        yield {
            "transaction_factory": transaction.TransactionFactory(settings_.db_dsn),
            "settings": settings_,
        }

    app_ = fastapi.FastAPI()

    app_.include_router(endpoints.router)
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=settings_.cors_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_
