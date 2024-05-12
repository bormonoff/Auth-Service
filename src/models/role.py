import uuid
from datetime import datetime

from core.config import get_settings
from db.postgres.session_handler import session_handler
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID


class Role(session_handler.base):
    __tablename__ = "role"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(
        String(get_settings().ROLE_TITLE_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    description = Column(String(get_settings().ROLE_TITLE_MAX_LENGTH))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
