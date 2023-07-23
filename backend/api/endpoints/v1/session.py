import fastapi

from .. import schemas

router = fastapi.APIRouter()

__all__ = ["router"]


EXAMPLE_SESSION = schemas.Session(
    id="abcd-efgh",
    members=[
        schemas.User(id="1", name="Federico", email="john@example.com"),
        schemas.User(id="2", name="Nathemis", email="john@example.com"),
    ],
)


@router.get("")
def list_sessions() -> list[schemas.Session]:
    return [EXAMPLE_SESSION]


@router.post("")
def create_session(session_id: str = fastapi.Body(embed=True)) -> schemas.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}")
def get_session(session_id: str) -> schemas.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}/join")
def join_session() -> schemas.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}/next_movie")
def get_next_movie() -> schemas.Movie:
    return schemas.Movie(
        id="foo", title="2001 Space Odyssey", image_url="https://example.com/my-img.png"
    )


@router.post("/{session_id}/movie/{movie_id}")
def vote_for_movie(vote: schemas.Vote) -> str:
    return "ok"


@router.get("/{session_id}/matches")
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
