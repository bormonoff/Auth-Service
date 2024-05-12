from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.config import get_settings


class AccessInSchema(BaseModel):
    """Schema for an input data with validation."""

    user_login: str = Field(
        pattern=get_settings().LOGIN_PATTERN,
        description=f"User login. Letters and digits only. {get_settings().LOGIN_MIN_LENGTH}-{get_settings().LOGIN_MAX_LENGTH} characters long.",
    )
    role_title: str = Field(
        pattern=get_settings().ROLE_TITLE_PATTERN,
        description=f"Role title. Letters and digits only. {get_settings().ROLE_TITLE_MIN_LENGTH}-{get_settings().ROLE_TITLE_MAX_LENGTH} characters long.",
    )


class AccessDBSchema(BaseModel):
    """Schema for DB operations."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    user_id: UUID
    role_id: UUID


class ShowUserAccessSchema(BaseModel):
    """Schema with roles list for user."""

    user_login: str
    roles: list[str] = []
