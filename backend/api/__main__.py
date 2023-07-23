import fastapi

from . import endpoints


def app() -> fastapi.FastAPI:
    app_ = fastapi.FastAPI()

    app_.include_router(endpoints.router)

    return app_
