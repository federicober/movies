from . import v1
import fastapi

router = fastapi.APIRouter()

router.include_router(router=v1.router)

__all__ = ["router"]
