import asyncio

from movies.core import transaction
from movies.scraper import config


async def main(settings: config.ScraperSettings | None = None) -> None:
    if settings is None:
        settings = config.ScraperSettings()  # type: ignore  # noqa: PGH003

    async with transaction.TransactionFactory(settings.db_dsn)() as tx:
        # tx.movies.add()
        await tx.commit()


if __name__ == "__main__":
    asyncio.run(main())
