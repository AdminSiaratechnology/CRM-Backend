from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class IntegrationConnection(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "integration_connections"
    provider: Mapped[str] = mapped_column(String(120), index=True)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class IntegrationCredential(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "integration_credentials"
    provider: Mapped[str] = mapped_column(String(120), index=True)
    secret_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class IntegrationLog(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "integration_logs"
    provider: Mapped[str] = mapped_column(String(120), index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
