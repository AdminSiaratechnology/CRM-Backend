from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.middleware.auth_middleware import require_permission, get_current_user
from app.schemas.auth import CurrentUser
from app.schemas.permission import (
    PermissionCreate, 
    PermissionUpdate, 
    PermissionResponse, 
    ModulePermissions,
    RolePermissionsUpdate,
    RolePermissionsResponse,
    UserPermissionsResponse
)
from app.services.permission_service import PermissionService

router = APIRouter()
service = PermissionService()


@router.get("/", response_model=list[ModulePermissions])
def list_permissions(
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("permissions.view"))
):
    data = service.list_grouped(db, user)
    return success_response(data, "Permissions loaded")


@router.post("/", response_model=PermissionResponse)
def create_permission(
    payload: PermissionCreate, 
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("permissions.create"))
):
    record = service.create(db, user, payload)
    db.commit()
    db.refresh(record)
    return success_response(PermissionResponse.model_validate(record), "Permission created")


@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: str, 
    payload: PermissionUpdate, 
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("permissions.edit"))
):
    record = service.update(db, user, permission_id, payload)
    db.commit()
    db.refresh(record)
    return success_response(PermissionResponse.model_validate(record), "Permission updated")


@router.delete("/{permission_id}")
def delete_permission(
    permission_id: str, 
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("permissions.delete"))
):
    service.delete(db, user, permission_id)
    db.commit()
    return success_response(None, "Permission deleted")


@router.get("/roles/{role_id}", response_model=RolePermissionsResponse)
def get_role_permissions_endpoint(
    role_id: str,
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("roles.manage_permissions"))
):
    data = service.get_role_permissions(db, user, role_id)
    return success_response(data, "Role permissions loaded")


@router.put("/roles/{role_id}", response_model=RolePermissionsResponse)
def update_role_permissions_endpoint(
    role_id: str,
    payload: RolePermissionsUpdate,
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(require_permission("roles.manage_permissions"))
):
    data = service.update_role_permissions(db, user, role_id, payload.permission_ids)
    db.commit()
    return success_response(data, "Role permissions updated")


@router.get("/me", response_model=UserPermissionsResponse)
def get_my_permissions(
    db: Session = Depends(get_db), 
    user: CurrentUser = Depends(get_current_user)
):
    permissions = service.get_user_permissions(db, user)
    return success_response({"permissions": permissions}, "User permissions loaded")
