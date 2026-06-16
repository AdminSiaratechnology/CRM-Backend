from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Permission(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "permissions"
    code: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(255))
