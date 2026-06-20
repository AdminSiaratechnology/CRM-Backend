from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()
service = RoleService()


@router.get("/")
def list_roles(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("roles.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Roles loaded", meta)


@router.post("/")
def create_role(payload: RoleCreate, db: Session = Depends(get_db), user=Depends(require_permission("roles.create"))):
    record = service.create(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Role created")


@router.get("/{role_id}")
def get_role(role_id: str, db: Session = Depends(get_db), user=Depends(require_permission("roles.view"))):
    return success_response(service.get(db, user, role_id), "Role loaded")


@router.patch("/{role_id}")
def update_role(role_id: str, payload: RoleUpdate, db: Session = Depends(get_db), user=Depends(require_permission("roles.edit"))):
    record = service.update(db, user, role_id, payload.model_dump(exclude_unset=True))
    db.commit()
    return success_response(record, "Role updated")


@router.delete("/{role_id}")
def delete_role(role_id: str, db: Session = Depends(get_db), user=Depends(require_permission("roles.delete"))):
    record = service.delete(db, user, role_id)
    db.commit()
    return success_response(record, "Role deleted")
