import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.postgres.session_handler import session_handler
from models.role import Role
from models.user import User


class UserRoleModel(session_handler.base):
    __tablename__ = "user_role"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Role.id, ondelete="CASCADE"),
        nullable=False,
    )
    role = relationship("Role", foreign_keys="UserRoleModel.role_id")
    user = relationship("User", foreign_keys="UserRoleModel.user_id")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    UniqueConstraint(user_id, role_id, name="unique_role_for_user")
