import asyncio
import csv
import gzip
import logging

import httpx
import pydantic
from anyio import Path

# Download datasets from
# https://developer.imdb.com/non-commercial-datasets/

logger = logging.getLogger(__name__)


class MovieBasics(pydantic.BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: bool
    startYear: int | None
    endYear: int | None
    runtimeMinutes: int | None
    genres: list[str]

    @pydantic.field_validator("startYear", "endYear", "runtimeMinutes", mode="before")
    @classmethod
    def parse_null_values(cls, v: str) -> str | None:
        return None if v == "\\N" else v

    @pydantic.field_validator("genres", mode="before")
    @classmethod
    def parse_list_values(cls, v: str) -> list[str]:
        return v.split(",")


async def _ensure_dataset_is_downloaded(root_path: Path, dataset: str) -> bytes:
    filename = f"{dataset}.tsv.gz"

    tmp_path = root_path / filename
    url = f"https://datasets.imdbws.com/{filename}"
    if await tmp_path.is_file():
        return await tmp_path.read_bytes()

    resp = httpx.get(url)
    resp.raise_for_status()
    await tmp_path.write_bytes(resp.content)
    return resp.content


def parse_csv(decompressed: str) -> None:
    per_lines = decompressed.splitlines()
    reader = csv.reader(
        per_lines, delimiter="\t", quotechar="\x00", quoting=csv.QUOTE_NONE
    )
    headers = next(reader)
    logger.info("Header is %s", headers)
    for row in reader:
        as_dict = dict(zip(headers, row))
        try:
            movie = MovieBasics(**as_dict)  # type: ignore[arg-type]
        except:
            logger.exception(
                "Failed to parse line %r %r %r",
                row,
                as_dict,
            )
            raise
        # print(movie)


async def main() -> None:
    root_path = Path("tmp")
    await root_path.mkdir(exist_ok=True, parents=True)
    dataset = "title.basics"

    compressed = await _ensure_dataset_is_downloaded(root_path, dataset)
    decompressed = gzip.decompress(compressed).decode("utf-8")
    parse_csv(decompressed)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    asyncio.run(main())
