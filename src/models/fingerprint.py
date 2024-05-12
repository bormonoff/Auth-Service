import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.config import get_settings
from db.postgres.session_handler import session_handler


class Fingerprint(session_handler.base):
    __tablename__ = "fingerprint"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    fingerprint = Column(
        String(get_settings().FINGERPRINT_MAX_LENGTH),
        unique=False,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    refresh_token = relationship(
        "RefreshToken",
        uselist=False,
    )
    user = relationship("User", back_populates="fingerprints")
