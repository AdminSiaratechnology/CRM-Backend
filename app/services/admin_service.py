from sqlalchemy.orm import Session
import json

from app.core.exceptions import AppError
from app.core.pagination import PaginationParams
from app.core.security import hash_password
from app.core.tenant import scoped_filters
from app.models.branch import Branch
from app.models.manager import Manager
from app.models.role import Role
from app.models.permission import Permission, UserPermission
from app.repositories.admin import PermissionsRepository, RolesRepository, UsersRepository
from app.schemas.auth import CurrentUser


class AdminService:
    def __init__(self):
        self.users = UsersRepository()
        self.roles = RolesRepository()
        self.permissions = PermissionsRepository()

    def _enrich_user(self, db: Session, user_obj) -> dict:
        """Convert user ORM object to dict with related entity details."""
        matrix_val = None
        if user_obj.permissions_matrix:
            try:
                matrix_val = json.loads(user_obj.permissions_matrix)
            except Exception:
                matrix_val = user_obj.permissions_matrix
                
        user_dict = {
            "id": user_obj.id,
            "name": user_obj.name,
            "email": user_obj.email,
            "mobile": user_obj.mobile,
            "status": user_obj.status,
            "login_access": user_obj.login_access,
            "gps_access": user_obj.gps_access,
            "monthly_target": user_obj.monthly_target,
            "created_at": user_obj.created_at.isoformat() if user_obj.created_at else None,
            "updated_at": user_obj.updated_at.isoformat() if user_obj.updated_at else None,
            "created_by_id": user_obj.created_by_id,
            "updated_by_id": user_obj.updated_by_id,
            "agency_name": user_obj.agency_name,
            "is_superuser": user_obj.is_superuser,
            "permissions_matrix": matrix_val,
            "role_id": user_obj.role_id,
            "branch_id": user_obj.branch_id,
            "manager_id": user_obj.manager_id,
            "role": None,
            "branch": None,
            "manager": None,
        }
        
        # Fetch and add role details if role_id exists
        if user_obj.role_id:
            try:
                role = db.query(Role).filter_by(id=user_obj.role_id).first()
                if role:
                    user_dict["role"] = {"id": role.id, "name": role.name}
            except Exception:
                pass
        
        # Fetch and add branch details if branch_id exists
        if user_obj.branch_id:
            try:
                branch = db.query(Branch).filter_by(id=user_obj.branch_id).first()
                if branch:
                    user_dict["branch"] = {"id": branch.id, "name": branch.name}
            except Exception:
                pass
        
        # Fetch and add manager details if manager_id exists
        if user_obj.manager_id:
            try:
                manager = db.query(Manager).filter_by(id=user_obj.manager_id).first()
                if manager:
                    user_dict["manager"] = {"id": manager.id, "name": manager.name}
            except Exception:
                pass
        
        return user_dict

    def list_users(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        """List users with enriched related entity details."""
        rows, meta = self.users.list(db, scoped_filters(user), pagination)
        enriched_rows = [self._enrich_user(db, u) for u in rows]
        return enriched_rows, meta

    def create_user(self, db: Session, user: CurrentUser, payload: dict):
        # Support aliases/toggles
        if "superuser_privileges" in payload and payload["superuser_privileges"] is not None:
            payload["is_superuser"] = payload["superuser_privileges"]
        if "operational_status" in payload and payload["operational_status"] is not None:
            payload["login_access"] = payload["operational_status"]
            
        # Extract password and remove it from payload
        password = payload.pop("password", None)
        if not password:
            raise AppError("Password is required", error_code="PASSWORD_REQUIRED")
            
        # Extract permissions and matrix from payload
        permissions_payload = payload.pop("permissions", None)
        matrix_payload = payload.pop("permissions_matrix", None)
        
        # Remove any extra fields not in the User model
        allowed_fields = {
            "name", "email", "mobile", "role_id", "branch_id", "manager_id", 
            "status", "login_access", "gps_access", "monthly_target",
            "agency_name", "is_superuser"
        }
        cleaned_payload = {k: v for k, v in payload.items() if k in allowed_fields}
        
        # Handle matrix serialization
        if matrix_payload is not None:
            if isinstance(matrix_payload, dict):
                cleaned_payload["permissions_matrix"] = json.dumps(matrix_payload)
            else:
                cleaned_payload["permissions_matrix"] = str(matrix_payload)
                
        created_user = self.users.create(db, {
            **cleaned_payload,
            **scoped_filters(user),
            "password_hash": hash_password(password),
            "created_by_id": user.user_id,
            "updated_by_id": user.user_id
        })
        db.flush()
        
        # Link direct permissions
        permission_codes_or_ids = list(permissions_payload) if permissions_payload else []
        
        if matrix_payload and isinstance(matrix_payload, dict):
            # Map action keys
            action_map = {
                "create": "create",
                "read": "view",
                "view": "view",
                "update": "edit",
                "edit": "edit",
                "delete": "delete"
            }
            for module_name, actions_dict in matrix_payload.items():
                if not isinstance(actions_dict, dict):
                    continue
                # Normalize module name: "STATE DASHBOARD" -> "state_dashboard"
                norm_module = module_name.strip().lower().replace(" ", "_")
                for action, is_granted in actions_dict.items():
                    if is_granted:
                        norm_action = action_map.get(action.strip().lower(), action.strip().lower())
                        permission_codes_or_ids.append(f"{norm_module}.{norm_action}")
                        
        if permission_codes_or_ids:
            unique_identifiers = list(set(permission_codes_or_ids))
            for identifier in unique_identifiers:
                perm = db.query(Permission).filter(
                    (Permission.id == identifier) | (Permission.code == identifier) | (Permission.name == identifier)
                ).first()
                
                # If the permission doesn't exist, create it dynamically
                if not perm:
                    parts = identifier.split(".")
                    module = parts[0] if len(parts) > 0 else "general"
                    action = parts[1] if len(parts) > 1 else "view"
                    perm = Permission(
                        tenant_id=user.tenant_id,
                        code=identifier,
                        label=identifier.replace(".", " ").title(),
                        module=module,
                        action=action,
                        name=identifier,
                        status="active"
                    )
                    db.add(perm)
                    db.flush()
                    
                # Associate UserPermission
                user_perm = UserPermission(
                    tenant_id=user.tenant_id,
                    user_id=created_user.id,
                    permission_id=perm.id,
                    created_by_id=user.user_id,
                    updated_by_id=user.user_id
                )
                db.add(user_perm)
            db.flush()
            
        # Return enriched user response
        return self._enrich_user(db, created_user)

    def list_roles(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.roles.list(db, scoped_filters(user), pagination)

    def create_role(self, db: Session, user: CurrentUser, payload: dict):
        return self.roles.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def list_permissions(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.permissions.list(db, scoped_filters(user), pagination)

    def get_user(self, db: Session, user: CurrentUser, user_id: str) -> dict:
        user_obj = self.users.get(db, scoped_filters(user), user_id)
        if not user_obj:
            raise AppError("User not found", error_code="USER_NOT_FOUND")
        return self._enrich_user(db, user_obj)

    def update_user(self, db: Session, user: CurrentUser, user_id: str, payload: dict) -> dict:
        user_obj = self.users.get(db, scoped_filters(user), user_id)
        if not user_obj:
            raise AppError("User not found", error_code="USER_NOT_FOUND")

        # Support aliases/toggles
        if "superuser_privileges" in payload and payload["superuser_privileges"] is not None:
            payload["is_superuser"] = payload["superuser_privileges"]
        if "operational_status" in payload and payload["operational_status"] is not None:
            payload["login_access"] = payload["operational_status"]

        # Extract password and remove it from payload if empty/not provided
        password = payload.pop("password", None)
        if password:
            payload["password_hash"] = hash_password(password)

        # Extract permissions and matrix from payload
        permissions_payload = payload.pop("permissions", None)
        matrix_payload = payload.pop("permissions_matrix", None)

        # Remove any extra fields not in the User model
        allowed_fields = {
            "name", "email", "mobile", "role_id", "branch_id", "manager_id", 
            "status", "login_access", "gps_access", "monthly_target",
            "agency_name", "is_superuser", "password_hash"
        }
        cleaned_payload = {k: v for k, v in payload.items() if k in allowed_fields}

        # Handle matrix serialization
        if matrix_payload is not None:
            if isinstance(matrix_payload, dict):
                cleaned_payload["permissions_matrix"] = json.dumps(matrix_payload)
            else:
                cleaned_payload["permissions_matrix"] = str(matrix_payload)

        # Update user record
        cleaned_payload["updated_by_id"] = user.user_id
        updated_user = self.users.update(db, user_obj, cleaned_payload)
        db.flush()

        # If permissions or permissions_matrix are updated
        if permissions_payload is not None or matrix_payload is not None:
            # Delete old permissions
            db.query(UserPermission).filter_by(user_id=user_id, tenant_id=user.tenant_id).delete()
            db.flush()

            permission_codes_or_ids = list(permissions_payload) if permissions_payload else []

            if matrix_payload and isinstance(matrix_payload, dict):
                # Map action keys
                action_map = {
                    "create": "create",
                    "read": "view",
                    "view": "view",
                    "update": "edit",
                    "edit": "edit",
                    "delete": "delete"
                }
                for module_name, actions_dict in matrix_payload.items():
                    if not isinstance(actions_dict, dict):
                        continue
                    # Normalize module name: "STATE DASHBOARD" -> "state_dashboard"
                    norm_module = module_name.strip().lower().replace(" ", "_")
                    for action, is_granted in actions_dict.items():
                        if is_granted:
                            norm_action = action_map.get(action.strip().lower(), action.strip().lower())
                            permission_codes_or_ids.append(f"{norm_module}.{norm_action}")

            if permission_codes_or_ids:
                unique_identifiers = list(set(permission_codes_or_ids))
                for identifier in unique_identifiers:
                    # Find the permission
                    perm = db.query(Permission).filter(
                        (Permission.id == identifier) | (Permission.code == identifier) | (Permission.name == identifier)
                    ).first()

                    # If the permission doesn't exist, create it dynamically
                    if not perm:
                        parts = identifier.split(".")
                        module = parts[0] if len(parts) > 0 else "general"
                        action = parts[1] if len(parts) > 1 else "view"
                        perm = Permission(
                            tenant_id=user.tenant_id,
                            code=identifier,
                            label=identifier.replace(".", " ").title(),
                            module=module,
                            action=action,
                            name=identifier,
                            status="active"
                        )
                        db.add(perm)
                        db.flush()

                    # Associate UserPermission
                    user_perm = UserPermission(
                        tenant_id=user.tenant_id,
                        user_id=updated_user.id,
                        permission_id=perm.id,
                        created_by_id=user.user_id,
                        updated_by_id=user.user_id
                    )
                    db.add(user_perm)
                db.flush()

        return self._enrich_user(db, updated_user)

    def delete_user(self, db: Session, user: CurrentUser, user_id: str) -> dict:
        user_obj = self.users.get(db, scoped_filters(user), user_id)
        if not user_obj:
            raise AppError("User not found", error_code="USER_NOT_FOUND")
        
        # Soft delete by setting status to 'deleted'
        self.users.update(db, user_obj, {"status": "deleted", "updated_by_id": user.user_id})
        db.flush()
        return self._enrich_user(db, user_obj)

