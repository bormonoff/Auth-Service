from uuid import UUID

from pydantic import BaseModel, Field


class UserTokenPair(BaseModel):
    login: str
    access_token: str
    refresh_token: str


class TokenHeader(BaseModel):
    typ: str = Field(default="JWT")
    alg: str = Field(default="HS256")


class TokenPayload(BaseModel):
    login: str
    body: str
    exp: str


class RefreshTokenInDB(BaseModel):
    id: UUID
    user_id: UUID
    refresh_token: str
