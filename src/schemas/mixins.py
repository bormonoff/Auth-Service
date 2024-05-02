from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class IdMixinSchema(BaseModel):
    id: UUID


class CreatedMixinSchema(BaseModel):
    created_at: datetime
    modified_at: datetime
