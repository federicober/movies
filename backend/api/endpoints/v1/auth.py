import fastapi

from .. import schemas

router = fastapi.APIRouter()

__all__ = ["router"]


@router.post("/login")
def login():
    pass
