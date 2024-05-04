import base64
from datetime import datetime, timedelta
from functools import lru_cache
from sqlite3 import IntegrityError
from typing import Annotated, Any

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.postgres import PostgresStorage, get_postgers_storage
from db.redis.redis_storage import RedisStorage, get_redis_storage
from models.user import User
from schemas.token import AcessTokenHeader, AcessTokenPayload
from schemas.user import UserBase
from util.hash_helper import get_hasher
from util.JWT_helper import get_jwt_helper


class TokenService:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database

    async def login(self, session: AsyncSession, user: UserBase):
        try:
            stmt = select(User).where(User.username == user.username)
            result = await self.database.execute(session=session, stmt=stmt)
            user_from_db = result.unique().scalars().first()
            get_hasher().verify(user_from_db.hashed_password, user.password)

            current_time = datetime.now()

            acess_token_exp_time = current_time + timedelta(hours=2)
            payload = AcessTokenPayload(login=user_from_db.username, role="admin", exp=str(acess_token_exp_time.timestamp()))
            JWThelper = await get_jwt_helper()
            acessToken = await JWThelper.encode(AcessTokenHeader(), payload)

            a = str(AcessTokenHeader().model_dump())
            header = base64.b64encode(a.encode("utf-8"))
        except IntegrityError as e:
            raise DBException(detail=e._message())


@lru_cache()
def get_token_service(
    redis: Annotated[Redis, Depends(get_redis_storage)],
    postgres: Annotated[PostgresStorage, Depends(get_postgers_storage)]
) -> TokenService:
    return TokenService(cache=redis, database=postgres)
