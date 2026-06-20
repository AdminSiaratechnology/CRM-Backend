from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.exceptions import success_response, AppError
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.branch import BranchCreate, BranchUpdate
from app.services.branch_service import BranchService

router = APIRouter()
service = BranchService()


@router.get("/")
def list_branches(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("branches.view"))):
    rows, meta = service.list(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Branches loaded", meta)


@router.post("/")
def create_branch(payload: BranchCreate, db: Session = Depends(get_db), user=Depends(require_permission("branches.create"))):
    try:
        record = service.create(db, user, payload.model_dump())
        db.commit()
        db.refresh(record)
        return success_response(record, "Branch created")
    except IntegrityError as e:
        db.rollback()
        if "code" in str(e).lower():
            raise AppError(
                "Branch code already exists",
                error_code="DUPLICATE_BRANCH_CODE"
            )
        raise AppError(
            "Failed to create branch due to duplicate or conflicting data",
            error_code="INTEGRITY_ERROR"
        )


@router.get("/{branch_id}")
def get_branch(branch_id: str, db: Session = Depends(get_db), user=Depends(require_permission("branches.view"))):
    return success_response(service.get(db, user, branch_id), "Branch loaded")


@router.patch("/{branch_id}")
def update_branch(branch_id: str, payload: BranchUpdate, db: Session = Depends(get_db), user=Depends(require_permission("branches.edit"))):
    record = service.update(db, user, branch_id, payload.model_dump(exclude_unset=True))
    db.commit()
    return success_response(record, "Branch updated")


@router.delete("/{branch_id}")
def delete_branch(branch_id: str, db: Session = Depends(get_db), user=Depends(require_permission("branches.delete"))):
    record = service.delete(db, user, branch_id)
    db.commit()
    return success_response(record, "Branch deleted")
