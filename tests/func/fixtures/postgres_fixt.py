import pytest

from testdata.db_schema import TABLES_SCHEMA, USER_CREATION


@pytest.fixture(scope="session")
async def prepare_db_tables(get_postgres_session):
    """Creates tables in the database."""
    for table_data in TABLES_SCHEMA:
        await get_postgres_session.execute(table_data["data"])


@pytest.fixture(scope="function")
async def prepare_users(get_postgres_session, empty_db_tables):
    """Registers users in the database public.user table."""
    for user in USER_CREATION:
        await get_postgres_session.execute(user)


@pytest.fixture(scope="function")
async def empty_db_tables(prepare_db_tables, get_postgres_session):
    """Cleans all tables in the database."""
    for table_data in TABLES_SCHEMA:
        await get_postgres_session.execute(
            f"TRUNCATE {table_data["table"]} CASCADE"
        )
