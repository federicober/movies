from . import v1
import fastapi

router = fastapi.APIRouter()

router.include_router(router=v1.router, prefix="/v1")

__all__ = ["router"]
