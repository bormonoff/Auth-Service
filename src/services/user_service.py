import random
import string
from datetime import datetime
from functools import lru_cache
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from core.exceptions import (DBException, UserHasBeenDeletedException,
                             UserNotFoundException)
from db.postgres.postgres import PostgresStorage
from models.user import User
from schemas.user import UserInDB, UserSaveToDB, UserSelf, UserSelfResponse


class UserService:
    def __init__(self, db_service, model):
        self.db_service = db_service(model)

    async def create_user(
        self, db: AsyncSession, user: UserSelf
    ) -> UserSelfResponse | HTTPException:
        """Create user in the database."""
        try:
            hashed_password = generate_password_hash(user.password)
            user_db_model = UserSaveToDB(
                **user.model_dump(), hashed_password=hashed_password
            )
            new_user = await self.db_service.create(db=db, obj=user_db_model)
            return new_user
        except IntegrityError as e:
            raise DBException(detail=e._message())

    async def get_user_from_db(
        self,
        db: AsyncSession,
        user: UUID,
    ) -> UserInDB | HTTPException:
        """Get the user from the database."""
        stmt = select(User).where(User.id == user)
        result = await self.db_service.execute(db=db, stmt=stmt)
        user_from_db = result.unique().scalars().first()
        if not user_from_db:
            raise UserNotFoundException
        if not user_from_db.is_active:
            raise UserHasBeenDeletedException
        return UserInDB.model_validate(user_from_db)

    async def update_user(
        self,
        db: AsyncSession,
        user: UUID,
        update_user_data: UserSelf,
    ) -> UserInDB:
        """Refresh user in the database."""
        try:
            updated_user_model = await self.get_user_from_db(db=db, user=user)

            if update_user_data.email:
                updated_user_model.email = update_user_data.email
            if update_user_data.username:
                updated_user_model.username = update_user_data.username
            if update_user_data.first_name:
                updated_user_model.first_name = update_user_data.first_name
            if update_user_data.last_name:
                updated_user_model.last_name = update_user_data.last_name
            if update_user_data.password:
                updated_user_model.hashed_password = generate_password_hash(
                    update_user_data.password
                )
            updated_user_model.modified_at = datetime.utcnow()

            await self.db_service.update(db=db, obj=updated_user_model)
        except IntegrityError as e:
            raise DBException(detail=e._message())
        return updated_user_model

    async def delete_user(self, db: AsyncSession, user: UUID) -> None:
        """Delete user in the database. User data become invalid."""
        user_from_db = await self.get_user_from_db(db=db, user=user)
        abracadabra = generate_password_hash(user_from_db.username)[:-20:-1]
        text = [
            random.choice(
                string.ascii_lowercase + string.digits
                if i != 5
                else string.ascii_uppercase
            )
            for i in range(30)
        ]
        update_data = UserInDB(
            id=user_from_db.id,
            username=abracadabra,
            email=("".join(text))[:-20:-1]
            + "@"
            + ("".join(text))[:-10:-1]
            + ".deleted",
            first_name=abracadabra,
            last_name=abracadabra,
            created_at=user_from_db.created_at,
            modified_at=datetime.utcnow(),
            hashed_password=user_from_db.hashed_password,
            is_active=False,
        )
        await self.db_service.update(db=db, obj=update_data)


@lru_cache()
def get_user_service() -> UserService:
    return UserService(db_service=PostgresStorage, model=User)
