import dataclasses

import sqlalchemy.exc
from sqlalchemy import insert
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from movies.core import exceptions
from movies.core.database.data_model import User
from movies.core.repositories import interfaces


@dataclasses.dataclass(frozen=True, slots=True)
class SessionRepo(interfaces.ISessionRepo):
    db_session: AsyncSession
