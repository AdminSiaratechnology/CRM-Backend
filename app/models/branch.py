from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Branch(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "branches"
    name: Mapped[str] = mapped_column(String(255), index=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    code: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # status is inherited from TenantScopedMixin
