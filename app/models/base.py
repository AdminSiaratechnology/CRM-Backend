from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class TenantScopedMixin(TimestampMixin):
    tenant_id: Mapped[str] = mapped_column(String(36), index=True, nullable=True)
    branch_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    team_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    owner_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    created_by_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    updated_by_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
