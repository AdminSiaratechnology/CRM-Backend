from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.exceptions import AppError
from app.core.permissions import has_permission
from app.core.security import decode_token
from app.models.permission import Permission, RolePermission, UserPermission
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import CurrentUser

bearer = HTTPBearer(auto_error=False)


def _get_user_permissions(db: Session, user_obj: User) -> List[str]:
    """Helper to get all active permissions for a user."""
    permission_names = set()
    
    # Get role permissions
    if user_obj.role_id:
        role_perms = db.query(RolePermission).filter(
            RolePermission.tenant_id == user_obj.tenant_id,
            RolePermission.role_id == user_obj.role_id
        ).all()
        
        for rp in role_perms:
            perm = db.query(Permission).filter(
                Permission.id == rp.permission_id,
                Permission.status == "active"
            ).first()
            if perm:
                permission_names.add(perm.name)
    
    # Get direct user permissions
    user_perms = db.query(UserPermission).filter(
        UserPermission.tenant_id == user_obj.tenant_id,
        UserPermission.user_id == user_obj.id
    ).all()
    
    for up in user_perms:
        perm = db.query(Permission).filter(
            Permission.id == up.permission_id,
            Permission.status == "active"
        ).first()
        if perm:
            permission_names.add(perm.name)
            
    return list(permission_names)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> CurrentUser:
    if not credentials or not credentials.credentials:
        raise AppError("Authentication required", "AUTH_REQUIRED", 401)
    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise AppError("Invalid or expired token", "INVALID_TOKEN", 401)
    user = db.query(User).filter(User.id == payload.get("sub"), User.deleted_at.is_(None)).first()
    if not user:
        raise AppError("Invalid user session", "INVALID_SESSION", 401)
    role = db.query(Role).filter(Role.id == user.role_id).first()
    
    # Get user permissions
    permissions = _get_user_permissions(db, user)
    
    return CurrentUser(
        user_id=user.id, 
        tenant_id=user.tenant_id, 
        branch_id=user.branch_id, 
        team_id=user.team_id, 
        role_name=role.name if role else "Viewer",
        role_id=user.role_id,
        scope=user.scope,
        permissions=permissions,
        is_superuser=user.is_superuser
    )



def require_permission(permission: str):
    def dependency(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not has_permission(user, permission):
            raise AppError("Permission denied", "FORBIDDEN", 403)
        return user

    return dependency
