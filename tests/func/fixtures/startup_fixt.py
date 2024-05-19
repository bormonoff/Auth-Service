import asyncio

import asyncpg
import pytest
from aiohttp import ClientSession
from redis.asyncio import Redis
from settings import get_settings


@pytest.fixture(scope="session")
def event_loop():
    """Makes event loop."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def get_http_session():
    """Creates and closes http client."""
    client = ClientSession()
    yield client
    await client.close()


@pytest.fixture(scope="session")
async def get_redis_session():
    """Creates and closes http client."""
    redis = Redis(
        host="localhost",
        port=get_settings().AUTH_REDIS_PORT,
        db=0,
        decode_responses=True,
    )
    yield redis
    await redis.aclose()


@pytest.fixture(scope="session")
async def get_postgres_session():
    """Creates and closes postgres client."""
    conn = await asyncpg.connect(
        host="localhost",
        port=get_settings().PG_PORT,
        user=get_settings().PG_USER,
        password=get_settings().PG_PASSWORD,
        database=get_settings().PG_DB,
    )
    yield conn
    await conn.close()
