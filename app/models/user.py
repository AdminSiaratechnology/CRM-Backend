from sqlalchemy import String, Boolean, Integer, Text
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
    branch_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    manager_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    login_access: Mapped[bool] = mapped_column(Boolean, default=True)
    gps_access: Mapped[bool] = mapped_column(Boolean, default=False)
    monthly_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    scope: Mapped[str] = mapped_column(String(50), default="OWN")
    agency_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    permissions_matrix: Mapped[str | None] = mapped_column(Text, nullable=True)

