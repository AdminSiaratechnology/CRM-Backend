from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Permission(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "permissions"
    
    code: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(255))
    module: Mapped[str] = mapped_column(String(100), index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "module", "action", name="uq_tenant_module_action"),
    )


class RolePermission(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "role_permissions"
    
    role_id: Mapped[str] = mapped_column(String(36), index=True)
    permission_id: Mapped[str] = mapped_column(String(36), index=True)
    
    __table_args__ = (
        UniqueConstraint("tenant_id", "role_id", "permission_id", name="uq_tenant_role_permission"),
    )
