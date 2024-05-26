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
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.config import get_settings
from core.exceptions import (FingerprintNotExists, InvalidToken,
                             InvalidUserOrPassword, TokenNotFoundException,
                             UserNotFoundException)
from db.postgres.postgres import PostgresStorage, get_postgers_storage
from db.redis.redis_storage import get_redis_storage
from models.fingerprint import Fingerprint
from models.role import Role
from models.token import RefreshToken
from models.user import User
from models.user_role import UserRoleModel
from schemas.fingerprint import FingerprintInDB
from schemas.token import (AccessTokenPayload, RefreshTokenInDB,
                           RefreshTokenPayload, TokenHeader, UserTokenPair)
from schemas.user import UserBase, UserInDBAccess
from util.hash_helper import get_hasher
from util.JWT_helper import get_jwt_helper


class AuthService:
    def __init__(self, cache, database: PostgresStorage):
        self.cache = cache
        self.database = database
        self.refresh_token_table = RefreshToken
        self.access_table = UserRoleModel
        self.role_table = Role
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
            user_from_db = await self._get_user_with_relations_from_db(
                session=session, user_login=user.login
            )
            if not user_from_db:
                raise InvalidUserOrPassword
            current_user = UserInDBAccess.model_validate(user_from_db)
            get_hasher().verify(current_user.hashed_password, user.password)
            current_user_roles = [
                access.role.title for access in current_user.access
            ]
            tokens = await self.construct_tokens(
                login=current_user.login,
                roles=current_user_roles,
                fingerprint=fingerprint,
            )

            fingerprint_in_db = (
                await self._get_fingerprint_and_refresh_token_from_db(
                    session=session, fingerprint=fingerprint
                )
            )
            if not fingerprint_in_db:
                fingerprint_obj = FingerprintInDB(
                    id=uuid.uuid4(),
                    user_id=current_user.id,
                    fingerprint=fingerprint,
                )
                fingerprint_in_db = await self.database.create(
                    session=session,
                    obj=fingerprint_obj,
                    table=self.fingerprint_table,
                )
                refresh_token = RefreshTokenInDB(
                    id=uuid.uuid4(),
                    user_id=current_user.id,
                    fingerprint_id=fingerprint_obj.id,
                    refresh_token=tokens.refresh_token,
                )
                await self.database.create(
                    session=session,
                    obj=refresh_token,
                    table=self.refresh_token_table,
                )
            else:
                if fingerprint_in_db.refresh_token:
                    fingerprint_in_db.refresh_token.refresh_token = (
                        tokens.refresh_token
                    )
                else:
                    fingerprint_in_db.refresh_token = RefreshToken(
                        user_id=current_user.id,
                        fingerprint_id=fingerprint_in_db.id,
                        refresh_token=tokens.refresh_token,
                    )
                await session.commit()

            return tokens
        except IntegrityError:
            raise UserNotFoundException
        except VerifyMismatchError:
            raise InvalidUserOrPassword

    async def refresh(
        self, session: AsyncSession, refresh_token: str
    ) -> UserTokenPair:
        """Generates the new token pair using the refresh token."""
        try:
            get_jwt_helper().verify_token(token=refresh_token)
            refresh_token_from_db = await self._get_refresh_token_from_db(
                session, refresh_token=refresh_token
            )
            if not refresh_token_from_db:
                raise TokenNotFoundException
            refresh_token_payload = get_jwt_helper().decode_payload(
                token=refresh_token, token_schema=RefreshTokenPayload
            )
            user_from_db = await self._get_user_with_relations_from_db(
                session=session, user_login=refresh_token_payload.sub
            )
            if not user_from_db:
                raise InvalidUserOrPassword
            current_user = UserInDBAccess.model_validate(user_from_db)
            current_user_roles = [
                access.role.title for access in current_user.access
            ]
            tokens = await self.construct_tokens(
                login=refresh_token_payload.sub,
                fingerprint=refresh_token_payload.fingerprint,
                roles=current_user_roles,
            )
            updated_token = RefreshTokenInDB(
                id=uuid.UUID(str(refresh_token_from_db.id)),
                user_id=uuid.UUID(str(refresh_token_from_db.user_id)),
                refresh_token=tokens.refresh_token,
                fingerprint_id=uuid.UUID(
                    str(refresh_token_from_db.fingerprint_id)
                ),
            )
            await self.database.update(
                session=session,
                obj=updated_token,
                table=self.refresh_token_table,
            )
            return tokens
        except (ValueError, binascii.Error):
            raise InvalidToken

    async def logout(
        self, session: AsyncSession, access_token: str, logout_everywhere: bool
    ) -> None:
        """Removes the current user session."""
        try:
            access_token_payload = get_jwt_helper().decode_payload(
                token=access_token, token_schema=AccessTokenPayload
            )
            user = await self._get_user_with_relations_from_db(
                session=session, user_login=access_token_payload.sub
            )
            if not user:
                raise UserNotFoundException
            if logout_everywhere:
                stmt = (delete(self.refresh_token_table)).where(
                    self.refresh_token_table.user_id == user.id
                )
                await session.execute(statement=stmt)
                await session.commit()
            else:
                fingerprint = (
                    await self._get_fingerprint_and_refresh_token_from_db(
                        session=session,
                        fingerprint=access_token_payload.fingerprint,
                    )
                )
                if not fingerprint:
                    raise FingerprintNotExists
                if not fingerprint.refresh_token:
                    raise TokenNotFoundException
                await session.delete(fingerprint.refresh_token)
                await session.commit()
            await self.cache.put_to_cache(
                access_token, "deleted", self.token_lifetime
            )
        except (ValueError, binascii.Error):
            raise InvalidToken

    async def construct_tokens(
        self,
        login: str,
        fingerprint: str,
        roles: list[str],
    ) -> UserTokenPair:
        """Constucts a new token pair for a target user."""
        current_time = datetime.now(timezone.utc)

        acess_token_exp_time = current_time + timedelta(
            hours=get_settings().ACESS_TOKEN_LIFETIME
        )
        payload = AccessTokenPayload(
            sub=login,
            fingerprint=fingerprint,
            roles=roles,
            exp=str(acess_token_exp_time.timestamp()),
        )
        acess_token = get_jwt_helper().encode(TokenHeader(), payload)

        refresh_token_exp_time = current_time + timedelta(
            days=get_settings().REFRESH_TOKEN_LIFETIME
        )
        payload = RefreshTokenPayload(
            sub=login,
            fingerprint=fingerprint,
            exp=str(refresh_token_exp_time.timestamp()),
        )
        refresh_token = get_jwt_helper().encode(TokenHeader(), payload)

        return UserTokenPair(
            access_token=acess_token, refresh_token=refresh_token
        )

    async def _get_user_with_relations_from_db(
        self,
        session: AsyncSession,
        user_login: str,
    ) -> User | None:
        """Helper returns the user with related objects from the database."""
        stmt = (
            select(self.user_table)
            .where(self.user_table.login == user_login)
            .options(
                joinedload(self.user_table.access).joinedload(
                    self.access_table.role
                ),
                joinedload(self.user_table.fingerprints).joinedload(
                    self.fingerprint_table.refresh_token
                ),
            )
        )
        result = await self.database.execute(session=session, stmt=stmt)
        return result.unique().scalars().one_or_none()

    async def _get_fingerprint_and_refresh_token_from_db(
        self, session: AsyncSession, fingerprint: str
    ) -> Fingerprint | None:
        """Helper returns the fingerprint from the database."""
        stmt = (
            select(self.fingerprint_table)
            .where(self.fingerprint_table.fingerprint == fingerprint)
            .options(joinedload(self.fingerprint_table.refresh_token))
        )
        result = await self.database.execute(session=session, stmt=stmt)
        return result.unique().scalars().first()

    async def _get_refresh_token_from_db(
        self,
        session: AsyncSession,
        refresh_token: str,
    ) -> RefreshToken | None:
        """Helper returns the token from the database."""
        stmt = select(self.refresh_token_table).where(
            self.refresh_token_table.refresh_token == refresh_token
        )
        results = await self.database.execute(session=session, stmt=stmt)
        return results.scalars().first()


@lru_cache()
def get_auth_service(
    redis: Annotated[Redis, Depends(get_redis_storage)],
    postgres: Annotated[PostgresStorage, Depends(get_postgers_storage)],
) -> AuthService:
    return AuthService(cache=redis, database=postgres)
