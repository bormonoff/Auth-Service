from sqlalchemy import MetaData

from db.postgres.session_handler import session_handler


async def create_database() -> None:
    async with session_handler.engine.begin() as conn:
        metadata = MetaData(schema="public")
        await conn.run_sync(metadata.reflect)
        if "public.user" not in metadata.tables.keys():
            await conn.run_sync(session_handler.base.metadata.create_all)


async def purge_database() -> None:
    async with session_handler.engine.begin() as conn:
        await conn.run_sync(session_handler.Base.metadata.drop_all)
