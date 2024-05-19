import pytest
from testdata.auth import (
    GET_REFRESH_TOKEN_REQUEST,
    INSERT_SUPERUSER_FINGERPRINT_REQUEST,
    INSERT_SUPERUSER_REFRESH_TOKEN_REQUEST,
)
from testdata.db_schema import TABLES_SCHEMA, USER_CREATION
from testdata.roles import INSERT_ROLE_DB


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


@pytest.fixture(scope="function")
async def insert_superuser_refresh_token(prepare_users, get_postgres_session):
    """Insert a superuser refresh token in the database."""
    await get_postgres_session.execute(INSERT_SUPERUSER_FINGERPRINT_REQUEST)
    await get_postgres_session.execute(INSERT_SUPERUSER_REFRESH_TOKEN_REQUEST)


@pytest.fixture(scope="function")
async def get_superuser_refresh_token(
    insert_superuser_refresh_token, get_postgres_session
):
    """Returns a superuser refresh token."""
    row = await get_postgres_session.fetchrow(GET_REFRESH_TOKEN_REQUEST)
    return row["refresh_token"]


@pytest.fixture(scope="function")
async def prepare_roles(empty_db_tables, get_postgres_session):
    """Inserts roles in the roles table."""
    for role in INSERT_ROLE_DB:
        await get_postgres_session.execute(role)
