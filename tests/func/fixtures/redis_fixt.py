import pytest
from redis import Redis


@pytest.fixture(scope="function")
async def redis_flush(get_redis_session: Redis):
    """Flushes the redis db."""
    await get_redis_session.flushall()


@pytest.fixture(scope="function")
async def redis_save_superuser_access_token(
    get_redis_session: Redis, prepare_headers_with_superuser_token: dict
):
    """Saves superuser access token to the redis db."""
    token = prepare_headers_with_superuser_token["Authorization"].replace(
        "Bearer ", ""
    )
    await get_redis_session.set(name=str(token), value="deleted")
