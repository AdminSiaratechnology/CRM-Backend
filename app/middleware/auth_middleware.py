from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppError
from app.core.permissions import has_permission
from app.core.security import decode_token
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import CurrentUser

bearer = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> CurrentUser:
    if not credentials or not credentials.credentials:
        raise AppError("Authentication required", "AUTH_REQUIRED", 401)
    payload = decode_token(credentials.credentials)
    user = db.query(User).filter(User.id == payload.get("sub"), User.deleted_at.is_(None)).first()
    if not user:
        raise AppError("Invalid user session", "INVALID_SESSION", 401)
    role = db.query(Role).filter(Role.id == user.role_id).first()
    return CurrentUser(user_id=user.id, tenant_id=user.tenant_id, branch_id=user.branch_id, team_id=user.team_id, role_name=role.name if role else "Viewer", scope=user.scope)


def require_permission(permission: str):
    def dependency(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not has_permission(user.role_name, permission):
            raise AppError("Permission denied", "FORBIDDEN", 403)
        return user

    return dependency
