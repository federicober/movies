from typing import Literal

import pytest


@pytest.fixture()
def anyio_backend() -> Literal["asyncio"]:
    return "asyncio"
