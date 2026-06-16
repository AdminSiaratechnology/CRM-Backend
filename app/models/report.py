from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class SavedReport(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "saved_reports"
    name: Mapped[str] = mapped_column(String(255), index=True)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class DashboardWidget(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dashboard_widgets"
    name: Mapped[str] = mapped_column(String(255), index=True)
    config_json: Mapped[str | None] = mapped_column(Text, nullable=True)
