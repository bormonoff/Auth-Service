from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AcessTokenHeader(BaseModel):
    typ: str = Field(default="JWT")
    alg: str = Field(default="HS256")


class AcessTokenPayload(BaseModel):
    login: str
    role: str
    exp: str