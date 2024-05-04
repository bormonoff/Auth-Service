from redis.asyncio import Redis
from sqlalchemy import MetaData

from core.config import get_settings
from db.postgres.session_handler import session_handler
from db.redis import redis


async def create_database() -> None:
    async with session_handler.engine.begin() as conn:
        metadata = MetaData(schema="public")
        await conn.run_sync(metadata.reflect)
        if "public.user" not in metadata.tables.keys():
            await conn.run_sync(session_handler.base.metadata.create_all)

async def redis_startup():
    redis.redis = Redis(host=get_settings().REDIS_HOST,
                        port=get_settings().REDIS_PORT,
                        db=0, decode_responses=True)

async def redis_shutdown():
    redis.redis.close()


async def purge_database() -> None:
    async with session_handler.engine.begin() as conn:
        await conn.run_sync(session_handler.Base.metadata.drop_all)
