import asyncio

from api import database, models


async def migrate() -> None:
    async with database.get_engine().begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        await conn.commit()


def main() -> None:
    asyncio.run(migrate())


if __name__ == "__main__":
    main()
