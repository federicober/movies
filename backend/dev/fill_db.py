import asyncio
import logging

from api import crud, database, migrate, schemas

logger = logging.getLogger(__name__)

USERS = [
    schemas.user.CreateUser(
        username="federicober",
        password="foobar",  # noqa: S106
    )
]


async def main() -> None:
    await migrate.migrate()
    async with (await database.get_session_factory())() as db:
        for user in USERS:
            logger.info("Creating user %s", user.username)
            await crud.user.create_user(db, user)
        await db.commit()
    logger.info("All setup")


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    asyncio.run(main())
