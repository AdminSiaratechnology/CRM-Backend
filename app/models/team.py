from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Team(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "teams"
    name: Mapped[str] = mapped_column(String(255), index=True)
