import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db.postgres.session_handler import session_handler


class RefreshToken(session_handler.base):
    __tablename__ = "token"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
