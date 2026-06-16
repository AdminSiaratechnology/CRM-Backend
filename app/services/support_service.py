from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.repositories.support import TicketsRepository
from app.schemas.auth import CurrentUser


class SupportService:
    def __init__(self):
        self.tickets = TicketsRepository()

    def list_tickets(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.tickets.list(db, scoped_filters(user), pagination)

    def create_ticket(self, db: Session, user: CurrentUser, payload: dict):
        return self.tickets.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id, "status": payload.get("status", "New")})

    def update_ticket(self, db: Session, user: CurrentUser, ticket_id: str, payload: dict):
        ticket = self.tickets.get(db, scoped_filters(user), ticket_id)
        return self.tickets.update(db, ticket, {**payload, "updated_by_id": user.user_id})

    def assign_ticket(self, db: Session, user: CurrentUser, ticket_id: str, owner_id: str):
        ticket = self.tickets.get(db, scoped_filters(user), ticket_id)
        return self.tickets.update(db, ticket, {"owner_id": owner_id, "updated_by_id": user.user_id})

    def resolve_ticket(self, db: Session, user: CurrentUser, ticket_id: str):
        ticket = self.tickets.get(db, scoped_filters(user), ticket_id)
        return self.tickets.update(db, ticket, {"status": "Resolved", "updated_by_id": user.user_id})
