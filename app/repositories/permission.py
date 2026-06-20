from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.permission import Permission, RolePermission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Permission)

    def get_by_name(self, db: Session, name: str) -> Permission | None:
        return db.query(Permission).filter(Permission.name == name).first()

    def get_by_module_action(self, db: Session, tenant_id: str | None, module: str, action: str) -> Permission | None:
        return db.query(Permission).filter(
            Permission.tenant_id == tenant_id,
            Permission.module == module,
            Permission.action == action
        ).first()

    def list_grouped_by_module(self, db: Session, filters: dict) -> List[Dict]:
        query = select(Permission).filter_by(**filters, status="active")
        permissions = db.execute(query).scalars().all()
        
        grouped = {}
        for perm in permissions:
            if perm.module not in grouped:
                grouped[perm.module] = []
            grouped[perm.module].append(perm)
        
        result = []
        for module, perms in grouped.items():
            result.append({"module": module, "permissions": perms})
        
        return result


class RolePermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RolePermission)

    def get_by_role_id(self, db: Session, tenant_id: str, role_id: str) -> List[RolePermission]:
        return db.query(RolePermission).filter(
            RolePermission.tenant_id == tenant_id,
            RolePermission.role_id == role_id
        ).all()

    def delete_by_role_id(self, db: Session, tenant_id: str, role_id: str):
        db.query(RolePermission).filter(
            RolePermission.tenant_id == tenant_id,
            RolePermission.role_id == role_id
        ).delete()
        db.flush()
