from uuid import UUID

from pydantic import BaseModel

from schemas.mixins import CreatedMixinSchema


class FingerprintInDB(CreatedMixinSchema):
    id: UUID
    user_id: UUID
    fingerprint: str