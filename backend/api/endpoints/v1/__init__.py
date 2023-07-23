from . import auth, session

import fastapi

router = fastapi.APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(session.router, prefix="/session")
