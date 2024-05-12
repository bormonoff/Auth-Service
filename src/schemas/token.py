from uuid import UUID

from pydantic import BaseModel, Field


class UserTokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")


class TokenHeader(BaseModel):
    typ: str = Field(default="JWT")
    alg: str = Field(default="HS256")


class AccessTokenPayload(BaseModel):
    sub: str
    fingerprint: str
    roles: list[str]
    exp: str


class RefreshTokenPayload(BaseModel):
    sub: str
    fingerprint: str
    exp: str


class RefreshTokenInDB(BaseModel):
    id: UUID
    user_id: UUID
    fingerprint_id: UUID
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenCheckResponse(AccessTokenPayload):
    token: str
