from sqlalchemy.orm import Session

from app.core.audit import write_audit_log
from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.deal import Deal
from app.repositories.deals import DealsRepository
from app.schemas.auth import CurrentUser


class DealsService:
    def __init__(self):
        self.repository = DealsRepository()

    def list(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.repository.list(db, scoped_filters(user), pagination)

    def create(self, db: Session, user: CurrentUser, payload: dict):
        record = self.repository.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})
        write_audit_log(db, tenant_id=user.tenant_id, actor_id=user.user_id, module="deals", action="create", entity_id=record.id, after_data={"name": record.name})
        return record

    def get(self, db: Session, user: CurrentUser, record_id: str):
        return self.repository.get(db, scoped_filters(user), record_id)

    def update(self, db: Session, user: CurrentUser, record_id: str, payload: dict):
        record = self.get(db, user, record_id)
        return self.repository.update(db, record, {**payload, "updated_by_id": user.user_id})

    def mark_stage(self, db: Session, user: CurrentUser, record_id: str, stage: str):
        record = self.get(db, user, record_id)
        return self.repository.update(db, record, {"stage": stage, "updated_by_id": user.user_id})

    def mark_won(self, db: Session, user: CurrentUser, record_id: str):
        return self.mark_stage(db, user, record_id, "Won")

    def mark_lost(self, db: Session, user: CurrentUser, record_id: str):
        return self.mark_stage(db, user, record_id, "Lost")
