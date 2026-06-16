from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.repositories.tenant import TenantRepository
from app.schemas.auth import CurrentUser

# Columns that exist on the Tenant model (own + TimestampMixin)
_TENANT_COLUMNS = {"name"}


def _clean_payload(payload: dict) -> dict:
    return {k: v for k, v in payload.items() if k in _TENANT_COLUMNS and v is not None}


class TenantService:
    def __init__(self):
        self.repository = TenantRepository()

    def list(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        """List all tenants with pagination (soft-deleted excluded)."""
        return self.repository.list(db, {"deleted_at": None}, pagination)

    def create(self, db: Session, user: CurrentUser, payload: dict):
        """Create a new tenant — only pass valid Tenant columns."""
        return self.repository.create(db, _clean_payload(payload))

    def get(self, db: Session, user: CurrentUser, record_id: str):
        """Retrieve a tenant by ID (non-deleted)."""
        return self.repository.get(db, {"deleted_at": None}, record_id)

    def update(self, db: Session, user: CurrentUser, record_id: str, payload: dict):
        """Update a tenant."""
        record = self.get(db, user, record_id)
        if not record:
            return None
        return self.repository.update(db, record, _clean_payload(payload))

    def delete(self, db: Session, user: CurrentUser, record_id: str):
        """Soft delete a tenant by setting deleted_at."""
        from datetime import datetime
        record = self.get(db, user, record_id)
        if not record:
            return None
        return self.repository.update(db, record, {"deleted_at": datetime.utcnow()})
