from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.mixins import CreatedMixinSchema


class UserInDB(CreatedMixinSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    login: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    hashed_password: str


class UserInDBAccess(UserInDB):
    model_config = ConfigDict(from_attributes=True)
    access: list = []


class UserSaveToDB(BaseModel):
    login: str
    email: EmailStr
    first_name: str
    last_name: str
    hashed_password: str


class UserSelf(BaseModel):
    login: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserBase(BaseModel):
    login: str
    password: str


class UserLogin(BaseModel):
    login: str
    acess_token: str


class UserSelfResponse(BaseModel):
    login: str
    email: EmailStr
    first_name: str
    last_name: str


class UserLoginSchema(BaseModel):
    login: str
