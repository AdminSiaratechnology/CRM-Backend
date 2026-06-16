from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Role(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(120), index=True)
    code: Mapped[str] = mapped_column(String(120), unique=True, index=True)
