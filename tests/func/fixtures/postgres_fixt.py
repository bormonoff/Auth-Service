import pytest

from testdata.db_schema import TABLES_SCHEMA, USER_CREATION


@pytest.fixture(scope="session")
async def prepare_db_tables(get_postgres_session):
    for table_data in TABLES_SCHEMA:
        await get_postgres_session.execute(table_data["data"])


@pytest.fixture(scope="function")
async def prepare_users(get_postgres_session):
    """User registration in DB public.user table."""
    for user in USER_CREATION:
        await get_postgres_session.execute(user)


@pytest.fixture(scope="function")
async def empty_db_tables(prepare_db_tables, get_postgres_session):
    for table_data in TABLES_SCHEMA:
        await get_postgres_session.execute(
            f"TRUNCATE {table_data["table"]} CASCADE"
        )
