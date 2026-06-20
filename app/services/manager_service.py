from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.manager import Manager
from app.repositories.manager import ManagerRepository
from app.schemas.auth import CurrentUser

# Columns that actually exist on the Manager model
_MANAGER_COLUMNS = {
    "name", "email", "mobile", "status",
    "tenant_id", "branch_id", "team_id", "owner_id",
    "created_by_id", "updated_by_id",
}


def _clean_payload(payload: dict) -> dict:
    """Strip unknown keys from payload."""
    cleaned = {}
    for key, value in payload.items():
        if key in _MANAGER_COLUMNS:
            cleaned[key] = value
    return cleaned


class ManagerService:
    def __init__(self):
        self.repository = ManagerRepository()

    def list(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        """List managers with tenant scoped filters and pagination."""
        return self.repository.list(db, scoped_filters(user), pagination)

    def create(self, db: Session, user: CurrentUser, payload: dict):
        """Create a new manager."""
        scope = scoped_filters(user)
        data = _clean_payload(payload)
        data.update({
            **scope,
            "created_by_id": user.user_id,
            "updated_by_id": user.user_id,
        })
        return self.repository.create(db, data)

    def get(self, db: Session, user: CurrentUser, record_id: str):
        """Retrieve a manager by ID with tenant filters."""
        return self.repository.get(db, scoped_filters(user), record_id)

    def update(self, db: Session, user: CurrentUser, record_id: str, payload: dict):
        """Update a manager."""
        record = self.get(db, user, record_id)
        data = _clean_payload(payload)
        data["updated_by_id"] = user.user_id
        return self.repository.update(db, record, data)

    def delete(self, db: Session, user: CurrentUser, record_id: str):
        """Soft delete a manager by setting status to 'deleted'."""
        record = self.get(db, user, record_id)
        if not record:
            return None
        if hasattr(record, "status"):
            self.repository.update(db, record, {"status": "deleted", "updated_by_id": user.user_id})
        else:
            db.delete(record)
            db.flush()
        return record
