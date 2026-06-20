from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.core.pagination import PaginationParams
from app.core.security import hash_password
from app.core.tenant import scoped_filters
from app.models.branch import Branch
from app.models.manager import Manager
from app.models.role import Role
from app.repositories.admin import PermissionsRepository, RolesRepository, UsersRepository
from app.schemas.auth import CurrentUser


class AdminService:
    def __init__(self):
        self.users = UsersRepository()
        self.roles = RolesRepository()
        self.permissions = PermissionsRepository()

    def _enrich_user(self, db: Session, user_obj) -> dict:
        """Convert user ORM object to dict with related entity details."""
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
        # Extract password and remove it from payload
        password = payload.pop("password", None)
        if not password:
            raise AppError("Password is required", error_code="PASSWORD_REQUIRED")
        
        # Remove any extra fields not in the User model
        allowed_fields = {"name", "email", "mobile", "role_id", "branch_id", "manager_id", "status", "login_access", "gps_access", "monthly_target"}
        cleaned_payload = {k: v for k, v in payload.items() if k in allowed_fields}
        
        created_user = self.users.create(db, {
            **cleaned_payload,
            **scoped_filters(user),
            "password_hash": hash_password(password),
            "created_by_id": user.user_id,
            "updated_by_id": user.user_id
        })
        
        # Return enriched user response
        return self._enrich_user(db, created_user)

    def list_roles(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.roles.list(db, scoped_filters(user), pagination)

    def create_role(self, db: Session, user: CurrentUser, payload: dict):
        return self.roles.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def list_permissions(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.permissions.list(db, scoped_filters(user), pagination)
