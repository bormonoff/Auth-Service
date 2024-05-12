import base64
import json
from datetime import datetime, timezone
from functools import lru_cache
from typing import Annotated

from argon2.exceptions import VerifyMismatchError
from Cryptodome.Hash import HMAC, SHA256
from fastapi import Depends
from fastapi.security import SecurityScopes
from pydantic import BaseModel

from core.config import get_settings
from core.exceptions import ExpireToken, UnAuthorizedException
from schemas.token import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenCheckResponse,
)


class JWTHelper:
    """JWTHelper provides methods to encode, decode and verify the token."""

    def __init__(self):
        self.encoding = get_settings().JWT_CODE
        self.key = get_settings().JWT_SECRET.encode(self.encoding)

    def encode(self, header: BaseModel, payload: BaseModel) -> str:
        """Basic encode function.

        Gets the header and payload pydantic objects and returns a JWT token."""
        hasher = HMAC.new(self.key, digestmod=SHA256)

        encode_header = self.encode_basemodel(header)
        encode_payload = self.encode_basemodel(payload)

        combined_str = f"{encode_header.decode(self.encoding)}.{encode_payload.decode("utf-8")}"

        hasher.update(combined_str.encode(self.encoding))
        digest = hasher.hexdigest()

        return f"{combined_str}.{digest}"

    def decode_payload(
        self,
        token: str,
        token_schema: type[RefreshTokenPayload] | type[AccessTokenPayload],
    ) -> RefreshTokenPayload | AccessTokenPayload:
        """Gets a token and return string with it's payload data."""
        token_parts = token.split(".")
        decoded_str = base64.b64decode(token_parts[1]).decode(self.encoding)
        payload = token_schema(**(json.loads(decoded_str.replace("'", '"'))))
        self.verify_exp_time(payload=payload)
        return payload

    def verify_token(self, token: str) -> None:
        """Gets a token string and verifies it."""
        hasher = HMAC.new(self.key, digestmod=SHA256)

        token_parts = token.split(".")
        if len(token_parts) != 3:
            raise ValueError
        payload = f"{token_parts[0]}.{token_parts[1]}"
        hasher.update(payload.encode(self.encoding))
        hasher.hexverify(token_parts[2])

    def verify_exp_time(self, payload: BaseModel) -> None:
        """Helper verifies payload exp time."""
        now = datetime.now(timezone.utc).timestamp()
        if float(payload.exp) < now:
            raise ExpireToken

    def encode_basemodel(self, model: BaseModel) -> str:
        """Helper incapsulates pydantic serialization logic."""
        serialized_str = str(model.model_dump())
        return base64.b64encode(serialized_str.encode(self.encoding))


@lru_cache()
def get_jwt_helper() -> JWTHelper:
    return JWTHelper()


def token_check(
    access_token: Annotated[str, Depends(get_settings().oauth2_scheme)],
    jwthelper: Annotated[JWTHelper, Depends(get_jwt_helper)],
    security_scopes: SecurityScopes,
) -> TokenCheckResponse:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    try:
        jwthelper.verify_token(access_token)
    except VerifyMismatchError:
        raise UnAuthorizedException(
            detail="Could not validate credentials",
            authenticate_value=authenticate_value,
        )
    token_payload = jwthelper.decode_payload(
        access_token, token_schema=AccessTokenPayload
    )
    if not token_payload:
        raise UnAuthorizedException(
            detail="No payload in token",
            authenticate_value=authenticate_value,
        )
    for scope in security_scopes.scopes:
        if scope not in token_payload.roles:
            raise UnAuthorizedException(
                detail="Not enough permissions",
                authenticate_value=authenticate_value,
            )
    return TokenCheckResponse(token=access_token, **token_payload.model_dump())
