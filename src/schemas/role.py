from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from core.config import get_settings
from schemas.mixins import CreatedMixinSchema


class RoleTitleSchema(BaseModel):
    title: str


class RoleCreateSchema(BaseModel):
    title: str = Field(
        pattern=get_settings().ROLE_TITLE_PATTERN,
        description="Role title. Letters and digits only. 3-50 characters long.",
    )

    description: str = Field(
        default="", max_length=get_settings().ROLE_DESCRIPTION_MAX_LENGTH
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "auth_admin",
                    "description": "Manager for roles and gives roles to other users",
                }
            ]
        }
    }


class RoleUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "auth_admin",
                    "description": "Manager for roles and gives roles to other users",
                }
            ]
        }
    }

    @field_validator("title")
    @classmethod
    def title_validator(cls, title: str) -> str:
        if isinstance(title, str):
            RoleCreateSchema(title=title)
            return title
        raise ValueError


class RoleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str


class RoleDBSchema(CreatedMixinSchema, RoleResponseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
