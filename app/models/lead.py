from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Lead(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "leads"
    first_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    stage: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    requirement: Mapped[str | None] = mapped_column(Text, nullable=True)
