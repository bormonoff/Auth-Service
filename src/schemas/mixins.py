from datetime import datetime

from pydantic import BaseModel, Field


class CreatedMixinSchema(BaseModel):
    created_at: datetime = Field(default=datetime.utcnow())
    modified_at: datetime = Field(default=datetime.utcnow())
