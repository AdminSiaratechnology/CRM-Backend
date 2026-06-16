from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.security import hash_password
from app.core.tenant import scoped_filters
from app.repositories.admin import PermissionsRepository, RolesRepository, UsersRepository
from app.schemas.auth import CurrentUser


class AdminService:
    def __init__(self):
        self.users = UsersRepository()
        self.roles = RolesRepository()
        self.permissions = PermissionsRepository()

    def list_users(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.users.list(db, scoped_filters(user), pagination)

    def create_user(self, db: Session, user: CurrentUser, payload: dict):
        return self.users.create(db, {**payload, **scoped_filters(user), "password_hash": hash_password(payload["password"]), "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def list_roles(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.roles.list(db, scoped_filters(user), pagination)

    def create_role(self, db: Session, user: CurrentUser, payload: dict):
        return self.roles.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def list_permissions(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.permissions.list(db, scoped_filters(user), pagination)
