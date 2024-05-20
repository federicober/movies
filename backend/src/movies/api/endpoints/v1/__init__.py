import fastapi

from . import auth, session

router = fastapi.APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(session.router, prefix="/session")
