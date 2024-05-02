
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import get_settings


class SessionHandler:
    def __init__(self):
        self.base = declarative_base()
        self.engine = create_async_engine(
            get_settings().postgres_dsn, echo=True, future=True
        )
        self.session_factory =  sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_session(self):
        async with self.session_factory() as session:
            yield session

session_handler = SessionHandler()
