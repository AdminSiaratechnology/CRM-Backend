from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Document(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "documents"
    title: Mapped[str] = mapped_column(String(255), index=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    related_module: Mapped[str | None] = mapped_column(String(120), nullable=True)
    related_record_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
