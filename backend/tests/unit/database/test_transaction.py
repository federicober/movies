import pathlib

import pytest
from movies.core import exceptions, transaction

pytestmark = pytest.mark.anyio


@pytest.fixture()
def transaction_factory(db_dsn: pathlib.Path) -> transaction.TransactionFactory:
    transaction_factory_ = transaction.TransactionFactory(
        f"sqlite+aiosqlite:///{db_dsn}"
    )
    return transaction_factory_


async def test_transaction_allows_for_multiple_actions(
    transaction_factory: transaction.TransactionFactory,
) -> None:
    async with transaction_factory() as transaction:
        await transaction.users.create("user 1", "user1@example.org", "pass")
        await transaction.users.create("user 2", "user2@example.org", "pass")
        await transaction.commit()


async def test_transaction_allows_ensure_persinstence_when_commit(
    transaction_factory: transaction.TransactionFactory,
) -> None:
    email = "user1@example.org"
    async with transaction_factory() as transaction:
        await transaction.users.create("user 1", email, "pass")
        await transaction.commit()

    async with transaction_factory() as transaction:
        await transaction.users.get(email)


@pytest.mark.parametrize("commit", [True, False])
async def test_transaction_commit_and_rollback_closes_connection(
    transaction_factory: transaction.TransactionFactory, commit: bool
) -> None:
    email = "user1@example.org"
    async with transaction_factory() as transaction:
        await transaction.users.create("user 1", email, "pass")
        await (transaction.commit() if commit else transaction.rollback())
        with pytest.raises(RuntimeError):
            await transaction.users.get(email)


async def test_transaction_rollbacks_makes_no_changes(
    transaction_factory: transaction.TransactionFactory,
) -> None:
    email = "user1@example.org"
    async with transaction_factory() as transaction:
        await transaction.users.create("user 1", email, "pass")
        await transaction.rollback()

    async with transaction_factory() as transaction:
        with pytest.raises(exceptions.UserNotFound):
            await transaction.users.get(email)


async def test_transaction_does_not_implicitly_commits(
    transaction_factory: transaction.TransactionFactory,
) -> None:
    email = "user1@example.org"
    async with transaction_factory() as transaction:
        await transaction.users.create("user 1", email, "pass")

    async with transaction_factory() as transaction:
        with pytest.raises(exceptions.UserNotFound):
            await transaction.users.get(email)
