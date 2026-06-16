from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Workflow(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "workflows"
    name: Mapped[str] = mapped_column(String(255), index=True)


class WorkflowRun(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "workflow_runs"
    workflow_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)


class AssignmentRule(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "assignment_rules"
    name: Mapped[str] = mapped_column(String(255), index=True)


class ReminderRule(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "reminder_rules"
    name: Mapped[str] = mapped_column(String(255), index=True)


class WebhookEndpoint(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "webhook_endpoints"
    name: Mapped[str] = mapped_column(String(255), index=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
