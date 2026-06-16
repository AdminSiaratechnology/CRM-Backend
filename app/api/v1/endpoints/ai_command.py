from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.ai_command import RunEngineRequest
from app.services.ai_command_service import AiCommandService

router = APIRouter()
service = AiCommandService()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    return success_response(service.dashboard(db, user), "AI command dashboard loaded")


@router.get("/alerts")
def alerts(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_alerts(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI alerts loaded", meta)


@router.get("/recommendations")
def recommendations(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_recommendations(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI recommendations loaded", meta)


@router.get("/revenue-leaks")
def revenue_leaks(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_revenue_leaks(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI revenue leaks loaded", meta)


@router.get("/deal-risk")
def deal_risk(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_recommendations(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI deal risk loaded", meta)


@router.get("/customer-health")
def customer_health(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_customer_health(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI customer health loaded", meta)


@router.get("/business-predictions")
def business_predictions(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.view"))):
    rows, meta = service.list_predictions(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "AI business predictions loaded", meta)


@router.post("/run")
def run_engine(payload: RunEngineRequest, db: Session = Depends(get_db), user=Depends(require_permission("aiCommand.manage"))):
    return success_response(service.run(db, user, payload.trigger), "AI engine run queued")
