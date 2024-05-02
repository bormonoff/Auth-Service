from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.mixins import CreatedMixinSchema


class UserInDB(CreatedMixinSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    hashed_password: str


class UserSaveToDB(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    hashed_password: str


class UserSelf(BaseModel):

    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserSelfResponse(BaseModel):

    username: str
    email: EmailStr
    first_name: str
    last_name: str
