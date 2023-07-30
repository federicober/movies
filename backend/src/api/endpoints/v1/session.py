import random

import fastapi

from ... import schemas

router = fastapi.APIRouter()

__all__ = ["router"]


EXAMPLE_SESSION = schemas.Session(
    id="abcd-efgh",
    members=[
        schemas.user.User(id="1", username="federicober", email="john@example.com"),
        schemas.user.User(id="2", username="nathemis", email="john@example.com"),
    ],
)

EXAMPLE_MOVIES = [
    schemas.Movie(
        id="foo",
        title="2001 Space Odyssey",
        image_url="https://m.media-amazon.com/images/M/MV5BMmNlYzRiNDctZWNhMi00MzI4LThkZTctMTUzMmZkMmFmNThmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
    ),
    schemas.Movie(
        id="bar",
        title="Oppenheimer",
        image_url="https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg",
    ),
]


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
def get_next_movie(session_id: str) -> schemas.Movie:
    return random.choice(EXAMPLE_MOVIES)  # noqa: S311


@router.post("/{session_id}/movie/{movie_id}")
def vote_for_movie(session_id: str, vote: schemas.Vote) -> str:
    return "ok"


@router.get("/{session_id}/matches")
def get_session_matches(session_id: str) -> schemas.SessionMatches:
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
