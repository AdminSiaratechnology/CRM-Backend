from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.lead import LeadAssignRequest, LeadCreate, LeadStageRequest, LeadUpdate
from app.services.leads_service import LeadsService

router = APIRouter()
service = LeadsService()


@router.get("")
def list_leads(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("leads.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Leads loaded", meta)


@router.post("")
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), user=Depends(require_permission("leads.create"))):
    record = service.create(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Lead created")


@router.get("/{lead_id}")
def get_lead(lead_id: str, db: Session = Depends(get_db), user=Depends(require_permission("leads.view"))):
    return success_response(service.get(db, user, lead_id), "Lead loaded")


@router.patch("/{lead_id}")
def update_lead(lead_id: str, payload: LeadUpdate, db: Session = Depends(get_db), user=Depends(require_permission("leads.edit"))):
    record = service.update(db, user, lead_id, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "Lead updated")


@router.delete("/{lead_id}")
def delete_lead(lead_id: str, db: Session = Depends(get_db), user=Depends(require_permission("leads.delete"))):
    record = service.update(db, user, lead_id, {"deleted_at": "now"})
    db.commit()
    return success_response(record, "Lead archived")


@router.post("/{lead_id}/assign")
def assign_lead(lead_id: str, payload: LeadAssignRequest, db: Session = Depends(get_db), user=Depends(require_permission("leads.assign"))):
    record = service.assign(db, user, lead_id, payload.owner_id)
    db.commit()
    return success_response(record, "Lead assigned")


@router.post("/{lead_id}/convert")
def convert_lead(lead_id: str, db: Session = Depends(get_db), user=Depends(require_permission("leads.convert"))):
    result = service.convert(db, user, lead_id)
    db.commit()
    return success_response(result, "Lead converted")


@router.patch("/{lead_id}/stage")
def update_lead_stage(lead_id: str, payload: LeadStageRequest, db: Session = Depends(get_db), user=Depends(require_permission("leads.edit"))):
    record = service.update(db, user, lead_id, {"stage": payload.stage})
    db.commit()
    return success_response(record, "Lead stage updated")


@router.get("/pipeline")
def pipeline(db: Session = Depends(get_db), user=Depends(require_permission("leads.view"))):
    rows, _ = service.list(db, user, PaginationParams(page=1, limit=200))
    return success_response(rows, "Lead pipeline loaded")


@router.get("/reports")
def reports(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=1, limit=50))
    return success_response({"rows": rows}, "Lead reports loaded", meta)
