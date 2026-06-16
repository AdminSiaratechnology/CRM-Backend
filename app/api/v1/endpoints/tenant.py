from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.services.tenant_service import TenantService

router = APIRouter()
service = TenantService()


@router.get("/")
def list_tenants(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("tenants.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Tenants loaded", meta)


@router.post("/")
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db), user=Depends(require_permission("tenants.create"))):
    record = service.create(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Tenant created")


@router.get("/{tenant_id}")
def get_tenant(tenant_id: str, db: Session = Depends(get_db), user=Depends(require_permission("tenants.view"))):
    return success_response(service.get(db, user, tenant_id), "Tenant loaded")


@router.patch("/{tenant_id}")
def update_tenant(tenant_id: str, payload: TenantUpdate, db: Session = Depends(get_db), user=Depends(require_permission("tenants.edit"))):
    record = service.update(db, user, tenant_id, payload.model_dump(exclude_unset=True))
    db.commit()
    return success_response(record, "Tenant updated")


@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: str, db: Session = Depends(get_db), user=Depends(require_permission("tenants.delete"))):
    record = service.delete(db, user, tenant_id)
    db.commit()
    return success_response(record, "Tenant deleted")
