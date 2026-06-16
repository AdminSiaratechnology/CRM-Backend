from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.branch import Branch
from app.repositories.branch import BranchRepository
from app.schemas.auth import CurrentUser

# Columns that actually exist on the Branch model (own + TenantScopedMixin + TimestampMixin)
_BRANCH_COLUMNS = {
    "name", "code", "country", "state", "city", "address", "status",
    "tenant_id", "branch_id", "team_id", "owner_id",
    "created_by_id", "updated_by_id",
}


def _clean_payload(payload: dict) -> dict:
    """Strip unknown keys and map countryCode -> country."""
    # alias mapping from frontend form field names
    aliases = {"countryCode": "country"}
    cleaned = {}
    for key, value in payload.items():
        mapped_key = aliases.get(key, key)
        if mapped_key in _BRANCH_COLUMNS:
            cleaned[mapped_key] = value
    return cleaned


class BranchService:
    def __init__(self):
        self.repository = BranchRepository()

    def list(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        """List branches with tenant scoped filters and pagination."""
        return self.repository.list(db, scoped_filters(user), pagination)

    def create(self, db: Session, user: CurrentUser, payload: dict):
        """Create a new branch and write audit log."""
        scope = scoped_filters(user)
        data = _clean_payload(payload)
        data.update({
            **scope,
            "created_by_id": user.user_id,
            "updated_by_id": user.user_id,
        })
        return self.repository.create(db, data)

    def get(self, db: Session, user: CurrentUser, record_id: str):
        """Retrieve a branch by ID with tenant filters."""
        return self.repository.get(db, scoped_filters(user), record_id)

    def update(self, db: Session, user: CurrentUser, record_id: str, payload: dict):
        """Update a branch and write audit log."""
        record = self.get(db, user, record_id)
        data = _clean_payload(payload)
        data["updated_by_id"] = user.user_id
        return self.repository.update(db, record, data)

    def delete(self, db: Session, user: CurrentUser, record_id: str):
        """Soft delete a branch by setting status to 'deleted'."""
        record = self.get(db, user, record_id)
        if not record:
            return None
        if hasattr(record, "status"):
            self.repository.update(db, record, {"status": "deleted", "updated_by_id": user.user_id})
        else:
            db.delete(record)
            db.flush()
        return record
