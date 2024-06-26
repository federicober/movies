import dataclasses

import sqlalchemy.exc
from sqlalchemy import insert
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from movies.core import exceptions
from movies.core.database.data_model import Movie
from movies.core.repositories import interfaces


@dataclasses.dataclass(frozen=True, slots=True)
class MovieRepo(interfaces.IMovieRepo):
    db_session: AsyncSession

    async def add(self, reference: str, title: str, image_url: str) -> None:
        try:
            await self.db_session.execute(
                insert(Movie).values(
                    reference=reference,
                    title=title,
                    image_url=image_url,
                )
            )
        except sqlalchemy.exc.IntegrityError:
            raise exceptions.MovieAlreadyExists() from None
