import random

import fastapi

from movies.api import deps, schemas
from movies.core.repositories import interfaces

router = fastapi.APIRouter(dependencies=[fastapi.Depends(deps.get_current_user)])

__all__ = ["router"]


EXAMPLE_SESSION = schemas.session.Session(
    reference="abcd-efgh",
    members=[
        schemas.user.GetUserResponse(
            display_name="federicober",
            email="john@example.com",
        ),
        schemas.user.GetUserResponse(display_name="nathemis", email="john@example.com"),
    ],
)


EXAMPLE_MOVIES = [
    schemas.movie.Movie(
        title="2001 Space Odyssey",
        image_url="https://m.media-amazon.com/images/M/MV5BMmNlYzRiNDctZWNhMi00MzI4LThkZTctMTUzMmZkMmFmNThmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
    ),
    schemas.movie.Movie(
        title="Oppenheimer",
        image_url="https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg",
    ),
]


@router.get("")
def list_sessions() -> list[schemas.session.Session]:
    return [EXAMPLE_SESSION]


@router.post("")
def create_session(
    session_id: str = fastapi.Body(embed=True),
) -> schemas.session.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}")
def get_session(session_id: str) -> schemas.session.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}/join")
def join_session() -> schemas.session.Session:
    return EXAMPLE_SESSION


@router.get("/{session_id}/next_movie")
def get_next_movie(session_id: str) -> schemas.movie.Movie:
    return random.choice(EXAMPLE_MOVIES)  # noqa: S311


@router.post("/{session_id}/movie/{movie_id}")
def vote_for_movie(session_id: str, vote: schemas.session.Vote) -> str:
    return "ok"


@router.get("/{session_id}/matches")
def get_session_matches(session_id: str) -> schemas.session.SessionMatches:
    return schemas.session.SessionMatches(
        count=1,
        movies=[
            schemas.movie.Movie(
                title="2001 Space Odyssey",
                image_url="https://example.com/my-img.png",
            )
        ],
    )
