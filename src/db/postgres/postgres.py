from functools import lru_cache
from typing import Any, List, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.postgres.session_handler import session_handler
from db.postgres.storage import BaseStorage

ModelType = TypeVar("ModelType", bound=session_handler.base)


class PostgresStorage(BaseStorage):
    async def create(
        self, session: AsyncSession, obj: BaseModel, table: Any
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        db_obj = table(**obj_dict)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self, session: AsyncSession, obj: BaseModel, table: Any
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        conditions = [getattr(table, k) == v for k, v in obj_dict.items()]
        stmt = delete(table).where(and_(*conditions)).returning(table)
        result = await session.execute(statement=stmt)
        await session.commit()
        return result.scalar_one_or_none()

    async def execute(self, session: AsyncSession, stmt):
        result = await session.execute(statement=stmt)
        return result

    async def get(
        self, session: AsyncSession, obj: BaseModel, table: Any
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        conditions = [getattr(table, k) == v for k, v in obj_dict.items()]
        stmt = select(table).where(and_(*conditions))
        result = await session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_list(
        self,
        session: AsyncSession,
        table: Any,
        filters: dict | None = None,
        offset: int = 0,
        limit: int | None = None,
    ) -> List[ModelType] | None:
        if not filters:
            filters = {}
        conditions = [getattr(table, k) == v for k, v in filters.items()]
        stmt = select(table).where(and_(*conditions)).offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        results = await session.execute(stmt)
        return results.scalars().all()

    async def update(
        self, session: AsyncSession, obj: BaseModel, table: Any
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        stmt = update(table).where(table.id == obj.id).values(**obj_dict)
        await session.execute(stmt)
        await session.commit()
        stmt = select(table).where(table.id == obj.id)
        results = await session.execute(stmt)
        db_obj = results.scalar_one()
        await session.refresh(db_obj)
        return db_obj


@lru_cache()
def get_postgers_storage() -> PostgresStorage:
    return PostgresStorage()
