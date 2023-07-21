import fastapi

router = fastapi.APIRouter()

__all__ = ["router"]


@router.post("session")
def create_session():
    pass


@router.get("session/{session_id}/next_movie")
def get_next_movie():
    pass


@router.post("session/{session_id}/movie/{movie_id}")
def vote_for_movie():
    pass


@router.get("session/{session_id}/matches")
def get_session_matches():
    pass
