from sqlalchemy.orm import Session
from typing import List, Dict

from app.core.exceptions import AppError
from app.core.tenant import scoped_filters
from app.models.permission import Permission, RolePermission
from app.models.user import User
from app.repositories.permission import PermissionRepository, RolePermissionRepository
from app.repositories.role import RoleRepository
from app.schemas.auth import CurrentUser
from app.schemas.permission import PermissionCreate, PermissionUpdate

# Columns that actually exist on the Permission model
_PERMISSION_COLUMNS = {
    "module", "action", "name", "code", "label", "description", "status",
    "tenant_id", "branch_id", "team_id", "owner_id",
    "created_by_id", "updated_by_id",
}


def _clean_payload(payload: dict) -> dict:
    """Strip unknown keys."""
    cleaned = {}
    for key, value in payload.items():
        if key in _PERMISSION_COLUMNS:
            cleaned[key] = value
    return cleaned


class PermissionService:
    def __init__(self):
        self.permission_repository = PermissionRepository()
        self.role_permission_repository = RolePermissionRepository()
        self.role_repository = RoleRepository()

    def list_grouped(self, db: Session, user: CurrentUser):
        """List all permissions grouped by module."""
        return self.permission_repository.list_grouped_by_module(db, scoped_filters(user))

    def create(self, db: Session, user: CurrentUser, payload: PermissionCreate):
        """Create a new permission."""
        scope = scoped_filters(user)
        
        # Auto-generate name, code, label if not provided
        name = payload.name if payload.name else f"{payload.module}.{payload.action}"
        code = payload.code if payload.code else name
        label = payload.label if payload.label else name.replace(".", " ").title()
        
        # Check for duplicate
        existing = self.permission_repository.get_by_module_action(db, user.tenant_id, payload.module, payload.action)
        if existing:
            raise AppError("Permission with this module and action already exists", "DUPLICATE_PERMISSION", 409)
        
        data = _clean_payload(payload.model_dump())
        data.update({
            **scope,
            "name": name,
            "code": code,
            "label": label,
            "created_by_id": user.user_id,
            "updated_by_id": user.user_id,
            "status": payload.status or "active"
        })
        
        return self.permission_repository.create(db, data)

    def get(self, db: Session, user: CurrentUser, permission_id: str):
        """Get a permission by ID."""
        return self.permission_repository.get(db, scoped_filters(user), permission_id)

    def update(self, db: Session, user: CurrentUser, permission_id: str, payload: PermissionUpdate):
        """Update an existing permission."""
        record = self.get(db, user, permission_id)
        if not record:
            raise AppError("Permission not found", "NOT_FOUND", 404)
        
        data = _clean_payload(payload.model_dump(exclude_unset=True))
        
        # If module or action changes, regenerate name, code, label
        if payload.module or payload.action:
            new_module = payload.module or record.module
            new_action = payload.action or record.action
            data["name"] = f"{new_module}.{new_action}"
            data["code"] = data["name"]
            data["label"] = data["name"].replace(".", " ").title()
            
            # Check for duplicate
            existing = self.permission_repository.get_by_module_action(db, user.tenant_id, new_module, new_action)
            if existing and existing.id != permission_id:
                raise AppError("Permission with this module and action already exists", "DUPLICATE_PERMISSION", 409)
        
        data["updated_by_id"] = user.user_id
        return self.permission_repository.update(db, record, data)

    def delete(self, db: Session, user: CurrentUser, permission_id: str):
        """Soft delete a permission."""
        record = self.get(db, user, permission_id)
        if not record:
            raise AppError("Permission not found", "NOT_FOUND", 404)
        
        return self.permission_repository.update(db, record, {
            "status": "inactive",
            "updated_by_id": user.user_id
        })

    def get_role_permissions(self, db: Session, user: CurrentUser, role_id: str):
        """Get permissions assigned to a role."""
        # Verify role exists and belongs to tenant
        role = self.role_repository.get(db, scoped_filters(user), role_id)
        if not role:
            raise AppError("Role not found", "NOT_FOUND", 404)
        
        # Get assigned permissions
        role_perms = self.role_permission_repository.get_by_role_id(db, user.tenant_id, role_id)
        assigned_ids = [rp.permission_id for rp in role_perms]
        
        # Get all permissions grouped by module
        all_perms = self.list_grouped(db, user)
        
        return {"assigned_permission_ids": assigned_ids, "all_permissions": all_perms}

    def update_role_permissions(self, db: Session, user: CurrentUser, role_id: str, permission_ids: List[str]):
        """Update permissions for a role (transaction safe)."""
        # Verify role exists
        role = self.role_repository.get(db, scoped_filters(user), role_id)
        if not role:
            raise AppError("Role not found", "NOT_FOUND", 404)
        
        # Validate all permission_ids exist and belong to tenant
        scope = scoped_filters(user)
        for pid in permission_ids:
            perm = self.permission_repository.get(db, scope, pid)
            if not perm:
                raise AppError(f"Permission {pid} not found", "INVALID_PERMISSION", 400)
        
        # Delete old permissions
        self.role_permission_repository.delete_by_role_id(db, user.tenant_id, role_id)
        
        # Add new permissions
        for pid in permission_ids:
            rp_data = {
                "tenant_id": user.tenant_id,
                "role_id": role_id,
                "permission_id": pid,
                "created_by_id": user.user_id,
                "updated_by_id": user.user_id,
            }
            self.role_permission_repository.create(db, rp_data)
        
        return self.get_role_permissions(db, user, role_id)

    def get_user_permissions(self, db: Session, user: CurrentUser) -> List[str]:
        """Get all permissions for current user."""
        user_obj = db.query(User).filter(User.id == user.user_id).first()
        if not user_obj or not user_obj.role_id:
            return []
        
        role_perms = self.role_permission_repository.get_by_role_id(db, user.tenant_id, user_obj.role_id)
        
        permission_names = []
        for rp in role_perms:
            perm = self.permission_repository.get(db, {}, rp.permission_id)
            if perm and perm.status == "active":
                permission_names.append(perm.name)
        
        return permission_names
