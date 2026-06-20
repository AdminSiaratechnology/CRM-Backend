from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.admin import AdminUserCreate, AdminUserUpdate
from app.services.admin_service import AdminService

router = APIRouter()
service = AdminService()


@router.get("/users")
def list_users(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("admin.manage"))):
    rows, meta = service.list_users(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Users loaded", meta)


@router.post("/users")
def create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("admin.manage"))
):
    record = service.create_user(db, user, payload.model_dump())
    db.commit()
    return success_response(record, "User created")


@router.get("/users/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_permission("admin.manage"))
):
    record = service.get_user(db, user, user_id)
    return success_response(record, "User loaded")


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("admin.manage"))
):
    record = service.update_user(db, user, user_id, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "User updated")


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_permission("admin.manage"))
):
    record = service.delete_user(db, user, user_id)
    db.commit()
    return success_response(record, "User deleted")


@router.get("/roles")
def list_roles(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("admin.manage"))):
    rows, meta = service.list_roles(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Roles loaded", meta)


@router.post("/roles")
def create_role(payload: dict, db: Session = Depends(get_db), user=Depends(require_permission("admin.manage"))):
    record = service.create_role(db, user, payload)
    db.commit()
    db.refresh(record)
    return success_response(record, "Role created")


@router.get("/permissions")
def list_permissions(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("admin.manage"))):
    rows, meta = service.list_permissions(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Permissions loaded", meta)


@router.post("/permissions")
def create_permission(payload: dict, db: Session = Depends(get_db), user=Depends(require_permission("admin.manage"))):
    record = service.permissions.create(db, {**payload, "tenant_id": user.tenant_id, "created_by_id": user.user_id, "updated_by_id": user.user_id})
    db.commit()
    db.refresh(record)
    return success_response(record, "Permission created")
