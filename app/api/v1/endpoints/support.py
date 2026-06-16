from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.support import TicketCreate
from app.services.support_service import SupportService

router = APIRouter()
service = SupportService()


@router.get("/tickets")
def list_tickets(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("support.view"))):
    rows, meta = service.list_tickets(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Tickets loaded", meta)


@router.post("/tickets")
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), user=Depends(require_permission("support.create"))):
    record = service.create_ticket(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Ticket created")


@router.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, payload: TicketCreate, db: Session = Depends(get_db), user=Depends(require_permission("support.edit"))):
    record = service.update_ticket(db, user, ticket_id, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "Ticket updated")


@router.post("/tickets/{ticket_id}/assign")
def assign_ticket(ticket_id: str, payload: dict, db: Session = Depends(get_db), user=Depends(require_permission("support.edit"))):
    record = service.assign_ticket(db, user, ticket_id, payload["owner_id"])
    db.commit()
    return success_response(record, "Ticket assigned")


@router.post("/tickets/{ticket_id}/resolve")
def resolve_ticket(ticket_id: str, db: Session = Depends(get_db), user=Depends(require_permission("support.resolve"))):
    record = service.resolve_ticket(db, user, ticket_id)
    db.commit()
    return success_response(record, "Ticket resolved")


@router.get("/reports")
def support_reports(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    rows, meta = service.list_tickets(db, user, PaginationParams(page=1, limit=50))
    return success_response({"rows": rows}, "Support reports loaded", meta)
