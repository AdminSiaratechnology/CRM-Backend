from sqlalchemy.orm import Session

from app.models.deal import Deal
from app.models.finance import Invoice
from app.models.lead import Lead
from app.models.support import Ticket
from app.schemas.auth import CurrentUser


class DashboardService:
    def executive(self, db: Session, user: CurrentUser):
        where = {"tenant_id": user.tenant_id, "deleted_at": None}
        return {
            "total_leads": db.query(Lead).filter_by(**where).count(),
            "open_deals": db.query(Deal).filter_by(**where).count(),
            "open_tickets": db.query(Ticket).filter_by(**where).count(),
            "invoices": db.query(Invoice).filter_by(**where).count(),
        }
