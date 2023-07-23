import fastapi

from api import schemas

router = fastapi.APIRouter()

__all__ = ["router"]


@router.post("/login")
def login():
    pass


@router.post("/session")
def create_session(session_id: str = fastapi.Body(embed=True)) -> schemas.Session:
    return schemas.Session(id="abcd-efgh")


@router.get("/session/{session_id}/join")
def join_session() -> str:
    return "ok"


@router.get("/session/{session_id}/next_movie")
def get_next_movie() -> schemas.Movie:
    return schemas.Movie(
        id="foo", title="2001 Space Odyssey", image_url="https://example.com/my-img.png"
    )


@router.post("/session/{session_id}/movie/{movie_id}")
def vote_for_movie(vote: schemas.Vote) -> str:
    return "ok"


@router.get("/session/{session_id}/matches")
def get_session_matches() -> schemas.SessionMatches:
    return schemas.SessionMatches(
        count=1,
        movies=[
            schemas.Movie(
                id="foo",
                title="2001 Space Odyssey",
                image_url="https://example.com/my-img.png",
            )
        ],
    )
