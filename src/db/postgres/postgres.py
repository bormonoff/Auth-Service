from typing import List, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.postgres.session_handler import session_handler
from db.postgres.storage import BaseStorage

ModelType = TypeVar("ModelType", bound=session_handler.base)


class PostgresStorage(BaseStorage):
    def __init__(self, model):
        self.model = model

    async def create(
        self, db: AsyncSession, obj: BaseModel
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        db_obj = self.model(**obj_dict)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(
        self, db: AsyncSession, obj: BaseModel
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        conditions = [getattr(self.model, k) == v for k, v in obj_dict.items()]
        stmt = (
            delete(self.model).where(and_(*conditions)).returning(self.model)
        )
        result = await db.execute(statement=stmt)
        await db.commit()
        return result.scalar_one_or_none()

    async def execute(self, db: AsyncSession, stmt):
        result = await db.execute(statement=stmt)
        return result

    async def get(self, db: AsyncSession, obj: BaseModel) -> ModelType | None:
        obj_dict = obj.model_dump()
        conditions = [getattr(self.model, k) == v for k, v in obj_dict.items()]
        stmt = select(self.model).where(and_(*conditions))
        result = await db.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        filters: dict | None = None,
        offset: int = 0,
        limit: int | None = None,
    ) -> List[ModelType] | None:
        if not filters:
            filters = {}
        conditions = [getattr(self.model, k) == v for k, v in filters.items()]
        stmt = select(self.model).where(and_(*conditions)).offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        results = await db.execute(stmt)
        return results.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        obj: BaseModel,
    ) -> ModelType | None:
        obj_dict = obj.model_dump()
        stmt = (
            update(self.model)
            .where(self.model.id == obj.id)
            .values(**obj_dict)
        )
        await db.execute(stmt)
        await db.commit()
        stmt = select(self.model).where(self.model.id == obj.id)
        results = await db.execute(stmt)
        db_obj = results.scalar_one()
        await db.refresh(db_obj)
        return db_obj
