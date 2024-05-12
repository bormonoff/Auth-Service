import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.config import get_settings
from db.postgres.session_handler import session_handler


class RefreshToken(session_handler.base):
    __tablename__ = "refresh_token"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    fingerprint_id = Column(UUID, ForeignKey("fingerprint.id"), nullable=False)
    refresh_token = Column(
        String(get_settings().REFRESH_TOKEN_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    UniqueConstraint(user_id, fingerprint_id, name="unique_fing_for_user")
    fingerprint = relationship(
        "Fingerprint",
        uselist=False,
    )
