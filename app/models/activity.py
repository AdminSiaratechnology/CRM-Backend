from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Task(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(String(255), index=True)
    due_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Meeting(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "meetings"
    title: Mapped[str] = mapped_column(String(255), index=True)
    starts_at: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Call(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "calls"
    subject: Mapped[str] = mapped_column(String(255), index=True)
    outcome: Mapped[str | None] = mapped_column(String(120), nullable=True)


class FollowUp(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "follow_ups"
    related_module: Mapped[str] = mapped_column(String(120), index=True)
    related_record_id: Mapped[str] = mapped_column(String(36), index=True)
    due_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
    outcome: Mapped[str | None] = mapped_column(Text, nullable=True)


class Note(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "notes"
    related_module: Mapped[str] = mapped_column(String(120), index=True)
    related_record_id: Mapped[str] = mapped_column(String(36), index=True)
    body: Mapped[str] = mapped_column(Text)
