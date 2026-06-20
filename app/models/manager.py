from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Manager(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "managers"
    name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    # status is inherited from TenantScopedMixin
