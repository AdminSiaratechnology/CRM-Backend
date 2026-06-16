from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Deal(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "deals"
    name: Mapped[str] = mapped_column(String(255), index=True)
    account_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    contact_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    stage: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)
    probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    expected_close_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
