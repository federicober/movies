import fastapi
from fastapi.middleware.cors import CORSMiddleware

from . import endpoints, settings


def app() -> fastapi.FastAPI:
    settings_ = settings.get_settings()
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
