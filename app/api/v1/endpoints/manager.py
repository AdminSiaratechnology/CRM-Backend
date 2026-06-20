from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.manager import ManagerCreate, ManagerUpdate
from app.services.manager_service import ManagerService

router = APIRouter()
service = ManagerService()


@router.get("/")
def list_managers(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("managers.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Managers loaded", meta)


@router.post("/")
def create_manager(payload: ManagerCreate, db: Session = Depends(get_db), user=Depends(require_permission("managers.create"))):
    record = service.create(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Manager created")


@router.get("/{manager_id}")
def get_manager(manager_id: str, db: Session = Depends(get_db), user=Depends(require_permission("managers.view"))):
    return success_response(service.get(db, user, manager_id), "Manager loaded")


@router.patch("/{manager_id}")
def update_manager(manager_id: str, payload: ManagerUpdate, db: Session = Depends(get_db), user=Depends(require_permission("managers.edit"))):
    record = service.update(db, user, manager_id, payload.model_dump(exclude_unset=True))
    db.commit()
    return success_response(record, "Manager updated")


@router.delete("/{manager_id}")
def delete_manager(manager_id: str, db: Session = Depends(get_db), user=Depends(require_permission("managers.delete"))):
    record = service.delete(db, user, manager_id)
    db.commit()
    return success_response(record, "Manager deleted")
