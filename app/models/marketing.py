from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Campaign(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "campaigns"
    name: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[str | None] = mapped_column(String(100), nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)


class Segment(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "segments"
    name: Mapped[str] = mapped_column(String(255), index=True)
    criteria_json: Mapped[str | None] = mapped_column(Text, nullable=True)


class LeadForm(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "lead_forms"
    name: Mapped[str] = mapped_column(String(255), index=True)


class LandingPage(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "landing_pages"
    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
