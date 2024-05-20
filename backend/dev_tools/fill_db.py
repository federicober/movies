import asyncio
import logging

from movies import crud, database, migrate, models, schemas

logger = logging.getLogger(__name__)


async def main() -> None:
    database.start_mappers()
    users = [
        models.User(
            username="federicober",
            email="joh.doe@example.org",
            password="foobar",  # noqa: S106
        )
    ]
    await migrate.migrate()
    async with (await database.get_session_factory())() as db:
        for user in users:
            logger.info("Creating user %s", user)
            await crud.user.create_user(db, user)
        await db.commit()
    logger.info("All setup")


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    asyncio.run(main())
