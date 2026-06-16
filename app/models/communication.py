from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class CommunicationSetting(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "communication_settings"
    channel: Mapped[str] = mapped_column(String(50), index=True)
    provider: Mapped[str | None] = mapped_column(String(100), nullable=True)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class CommunicationLog(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "communication_logs"
    channel: Mapped[str] = mapped_column(String(50), index=True)
    direction: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)


class CommunicationTemplate(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "communication_templates"
    channel: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text)


class EmailMessage(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "email_messages"
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)


class WhatsAppMessage(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "whatsapp_messages"
    recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)


class SMSMessage(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "sms_messages"
    recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)


class CallLog(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "call_logs"
    caller: Mapped[str | None] = mapped_column(String(255), nullable=True)
    receiver: Mapped[str | None] = mapped_column(String(255), nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(100), nullable=True)
