import fastapi
import pydantic

from . import v1

router = fastapi.APIRouter()

router.include_router(router=v1.router, prefix="/v1")

__all__ = ["router"]
