import binascii
import re
import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from sqlite3 import IntegrityError
from typing import Annotated

from argon2.exceptions import VerifyMismatchError
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from core.exceptions import (FingerprintExists, FingerprintNotExists,
                             InvalidToken, InvalidUserOrPassword,
                             TokenNotFoundException, UserNotFoundException)
from db.postgres.postgres import PostgresStorage, get_postgers_storage
from db.redis.redis_storage import get_redis_storage
from models.fingerprint import Fingerprint
from models.token import RefreshToken
from models.user import User
from schemas.fingerprint import FingerprintInDB
from schemas.token import (RefreshTokenInDB, TokenHeader, TokenPayload,
                           UserTokenPair)
from schemas.user import UserBase, UserInDB
from util.hash_helper import get_hasher
from util.JWT_helper import get_jwt_helper


class AuthService:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
        self.token_table = RefreshToken
        self.user_table = User
        self.fingerprint_table = Fingerprint
        self.token_lifetime = get_settings().ACESS_TOKEN_LIFETIME * 60

    async def login(
        self, session: AsyncSession, user: UserBase, fingerprint: str
    ) -> UserTokenPair:
        """Creates the new session.

        If verification successed, service returns generated tokens."""
        try:
            if not re.match(get_settings().LOGIN_PATTERN, user.login):
                raise InvalidUserOrPassword
            user_from_db = await self.get_user(session=session, user=user)
            if not user_from_db:
                raise InvalidUserOrPassword
            current_user = UserInDB.model_validate(user_from_db)
            get_hasher().verify(current_user.hashed_password, user.password)

            fingerprint_in_db = await self.get_fingerprint(session=session,
                                                           fingerprint=fingerprint)
            if fingerprint_in_db:
                raise FingerprintExists

            tokens = await self.construct_tokens(login=current_user.login,
                                                 fingerprint=fingerprint)
            token_obj = RefreshTokenInDB(
                id=uuid.uuid4(),
                user_id=current_user.id,
                refresh_token=tokens.refresh_token,
            )
            fingerpirnt_obj = FingerprintInDB(
                id=uuid.uuid4(),
                user_id=current_user.id,
                fingerprint=fingerprint,
            )

            await self.database.create(
                session=session, obj=token_obj, table=self.token_table
            )
            await self.database.create(
                session=session, obj=fingerpirnt_obj, table=self.fingerprint_table
            )
            return tokens
        except IntegrityError:
            raise UserNotFoundException
        except VerifyMismatchError:
            raise InvalidUserOrPassword

    async def refresh(
        self, session: AsyncSession, token: str
    ) -> UserTokenPair:
        """Generates the new token pair using the refresh token."""
        try:
            await get_jwt_helper().verify_token(token=token)
            payload = await get_jwt_helper().decode_payload(token=token)

            tokens = await self.construct_tokens(login=payload.login)
            token_from_db = await self.get_token(session, token=token)
            if not token_from_db:
                raise TokenNotFoundException

            updated_token = RefreshTokenInDB(
                id=token_from_db.id,
                user_id=token_from_db.user_id,
                refresh_token=token_from_db.refresh_token,
            )
            updated_token.refresh_token = tokens.refresh_token

            await self.database.update(
                session=session, obj=updated_token, table=self.token_table
            )
            return tokens
        except (ValueError, binascii.Error):
            raise InvalidToken

    async def logout(self, session: AsyncSession, token: str) -> None:
        """Removes the current user session."""
        try:
            await get_jwt_helper().verify_token(token=token)
            await get_jwt_helper().decode_payload(token=token)

            token_from_db = await self.get_token(session, token=token)
            if not token_from_db:
                raise TokenNotFoundException

            token_payload = await get_jwt_helper().decode_payload(token)
            fingerprint_from_db = await self.get_fingerprint(session, token_payload.body)
            if not fingerprint_from_db:
                raise FingerprintNotExists
            delete_token = RefreshTokenInDB(
                id=token_from_db.id,
                user_id=token_from_db.user_id,
                refresh_token=token_from_db.refresh_token,
            )
            delete_fingerprint = FingerprintInDB(
                id=fingerprint_from_db.id,
                user_id=fingerprint_from_db.user_id,
                fingerprint=fingerprint_from_db.fingerprint
            )
            await self.cache.put_to_cache(token, "deleted", self.token_lifetime)
            await self.database.delete(session, delete_token, self.token_table)
            await self.database.delete(session, delete_fingerprint, self.fingerprint_table)
        except (ValueError, binascii.Error):
            raise InvalidToken

    async def construct_tokens(
        self, login: str, fingerprint: str, roles: list[str] = ["admin", "user"]
    ) -> UserTokenPair:
        """Constucts a new token pair for a target user."""
        current_time = datetime.now(timezone.utc)

        roles_str = ",".join(roles)
        acess_token_exp_time = current_time + timedelta(
            hours=get_settings().ACESS_TOKEN_LIFETIME
        )
        payload = TokenPayload(
            login=login,
            body=roles_str,
            exp=str(acess_token_exp_time.timestamp()),
        )
        acess_token = await get_jwt_helper().encode(
            TokenHeader(), payload
        )

        refresh_token_exp_time = current_time + timedelta(
            days=get_settings().REFRESH_TOKEN_LIFETIME
        )
        payload = TokenPayload(
            login=login,
            body=fingerprint,
            exp=str(refresh_token_exp_time.timestamp()),
        )
        refresh_token = await get_jwt_helper().encode(
            TokenHeader(), payload
        )

        return UserTokenPair(
            login=login, access_token=acess_token, refresh_token=refresh_token
        )

    async def get_user(self, session: AsyncSession, user: UserBase) -> User:
        """Helper returns the user from the database."""
        stmt = select(self.user_table).where(
            self.user_table.login == user.login
        )
        result = await self.database.execute(session=session, stmt=stmt)
        return result.unique().scalars().first()

    async def get_fingerprint(self, session: AsyncSession, fingerprint: str) -> Fingerprint:
        """Helper returns the fingerprint from the database."""
        stmt = select(self.fingerprint_table).where(
            self.fingerprint_table.fingerprint == fingerprint
        )
        result = await self.database.execute(session=session, stmt=stmt)
        return result.unique().scalars().first()

    async def get_token(
        self, session: AsyncSession, token: str
    ) -> RefreshToken:
        """Helper returns the token from the database."""
        stmt = select(self.token_table).where(
            self.token_table.refresh_token == token
        )
        result = await self.database.execute(session=session, stmt=stmt)
        return result.unique().scalars().first()


@lru_cache()
def get_token_service(
    redis: Annotated[Redis, Depends(get_redis_storage)],
    postgres: Annotated[PostgresStorage, Depends(get_postgers_storage)],
) -> AuthService:
    return AuthService(cache=redis, database=postgres)
