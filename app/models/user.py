from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    mobile: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    scope: Mapped[str] = mapped_column(String(50), default="OWN")
