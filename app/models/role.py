from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Role(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(120), index=True)
    code: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_access_level: Mapped[str | None] = mapped_column(String(50), nullable=True)  # Tenant, Country, Region, Branch, Team, Own records
    permissions_matrix: Mapped[str | None] = mapped_column(Text, nullable=True)  # Comma-separated or JSON
