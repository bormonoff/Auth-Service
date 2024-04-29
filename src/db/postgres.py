from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import get_settings
from main import app

Base = declarative_base()
dsn = f"postgresql+asyncpg://{get_settings().pg_user}:{get_settings().pg_password}@{get_settings().pg_host}:{get_settings().pg_port}/{get_settings().pg_db}"
engine = create_async_engine(dsn, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def startup():
    from models.user import User

    await create_database()
