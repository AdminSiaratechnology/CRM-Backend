from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.deal import DealCreate, DealStageRequest
from app.services.deals_service import DealsService

router = APIRouter()
service = DealsService()


@router.get("")
def list_deals(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("deals.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Deals loaded", meta)


@router.post("")
def create_deal(payload: DealCreate, db: Session = Depends(get_db), user=Depends(require_permission("deals.create"))):
    record = service.create(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Deal created")


@router.get("/{deal_id}")
def get_deal(deal_id: str, db: Session = Depends(get_db), user=Depends(require_permission("deals.view"))):
    return success_response(service.get(db, user, deal_id), "Deal loaded")


@router.patch("/{deal_id}")
def update_deal(deal_id: str, payload: DealCreate, db: Session = Depends(get_db), user=Depends(require_permission("deals.edit"))):
    record = service.update(db, user, deal_id, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "Deal updated")


@router.patch("/{deal_id}/stage")
def update_stage(deal_id: str, payload: DealStageRequest, db: Session = Depends(get_db), user=Depends(require_permission("deals.edit"))):
    record = service.mark_stage(db, user, deal_id, payload.stage)
    db.commit()
    return success_response(record, "Deal stage updated")


@router.post("/{deal_id}/mark-won")
def mark_won(deal_id: str, db: Session = Depends(get_db), user=Depends(require_permission("deals.approve"))):
    record = service.mark_won(db, user, deal_id)
    db.commit()
    return success_response(record, "Deal marked won")


@router.post("/{deal_id}/mark-lost")
def mark_lost(deal_id: str, db: Session = Depends(get_db), user=Depends(require_permission("deals.approve"))):
    record = service.mark_lost(db, user, deal_id)
    db.commit()
    return success_response(record, "Deal marked lost")


@router.get("/pipeline")
def pipeline(db: Session = Depends(get_db), user=Depends(require_permission("deals.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=1, limit=200))
    return success_response({"rows": rows}, "Deal pipeline loaded", meta)


@router.get("/forecast")
def forecast(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    rows, _ = service.list(db, user, PaginationParams(page=1, limit=200))
    return success_response({"forecast": rows}, "Deal forecast loaded")


@router.get("/reports")
def reports(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=1, limit=50))
    return success_response({"rows": rows}, "Deal reports loaded", meta)
