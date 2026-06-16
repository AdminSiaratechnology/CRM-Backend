from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Ticket(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "tickets"
    subject: Mapped[str] = mapped_column(String(255), index=True)
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class SLA(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "sla_policies"
    name: Mapped[str] = mapped_column(String(255), index=True)


class EscalationRule(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "escalation_rules"
    name: Mapped[str] = mapped_column(String(255), index=True)


class KnowledgeBaseArticle(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "knowledge_base_articles"
    title: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
