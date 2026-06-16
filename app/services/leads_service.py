from sqlalchemy.orm import Session

from app.core.audit import write_audit_log
from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.account import Account
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.lead import Lead
from app.repositories.leads import LeadsRepository
from app.schemas.auth import CurrentUser


class LeadsService:
    def __init__(self):
        self.repository = LeadsRepository()

    def list(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.repository.list(db, scoped_filters(user), pagination)

    def create(self, db: Session, user: CurrentUser, payload: dict):
        record = self.repository.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})
        write_audit_log(db, tenant_id=user.tenant_id, actor_id=user.user_id, module="leads", action="create", entity_id=record.id, after_data={"full_name": record.full_name})
        return record

    def get(self, db: Session, user: CurrentUser, record_id: str):
        return self.repository.get(db, scoped_filters(user), record_id)

    def update(self, db: Session, user: CurrentUser, record_id: str, payload: dict):
        record = self.get(db, user, record_id)
        return self.repository.update(db, record, {**payload, "updated_by_id": user.user_id})

    def assign(self, db: Session, user: CurrentUser, record_id: str, owner_id: str):
        record = self.get(db, user, record_id)
        return self.repository.update(db, record, {"owner_id": owner_id, "updated_by_id": user.user_id})

    def convert(self, db: Session, user: CurrentUser, record_id: str):
        lead = self.get(db, user, record_id)
        contact = Contact(tenant_id=user.tenant_id, branch_id=lead.branch_id, team_id=lead.team_id, owner_id=lead.owner_id, created_by_id=user.user_id, updated_by_id=user.user_id, full_name=lead.full_name, email=lead.email, mobile=lead.mobile, company_name=lead.company)
        account = Account(tenant_id=user.tenant_id, branch_id=lead.branch_id, team_id=lead.team_id, owner_id=lead.owner_id, created_by_id=user.user_id, updated_by_id=user.user_id, company_name=lead.company or lead.full_name, industry=None)
        deal = Deal(tenant_id=user.tenant_id, branch_id=lead.branch_id, team_id=lead.team_id, owner_id=lead.owner_id, created_by_id=user.user_id, updated_by_id=user.user_id, name=f"{lead.company or lead.full_name} opportunity", stage="New Opportunity", value=None, probability=0)
        db.add_all([contact, account, deal])
        self.repository.update(db, lead, {"stage": "Converted", "updated_by_id": user.user_id})
        write_audit_log(db, tenant_id=user.tenant_id, actor_id=user.user_id, module="leads", action="convert", entity_id=lead.id, after_data={"contact_id": contact.id, "account_id": account.id, "deal_id": deal.id})
        return {"lead_id": lead.id, "contact_id": contact.id, "account_id": account.id, "deal_id": deal.id}
