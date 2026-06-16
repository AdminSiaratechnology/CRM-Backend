from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.dubai_finance import (
    DubaiFinanceApplicationCreate,
    DubaiFinanceApplicationUpdate,
    DubaiFinanceAssignRequest,
    DubaiFinanceBankSelectionCreate,
    DubaiFinanceBankStatusUpdate,
    DubaiFinanceBankSubmissionCreate,
    DubaiFinanceCommissionCreate,
    DubaiFinanceDecisionRequest,
    DubaiFinanceDocumentCreate,
    DubaiFinanceEligibilityRequest,
    DubaiFinanceDisbursalRequest,
)
from app.services.dubai_finance_service import DubaiFinanceService

router = APIRouter()
service = DubaiFinanceService()


@router.get("/applications")
def list_applications(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    rows, meta = service.list_applications(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Dubai finance applications loaded", meta)


@router.post("/applications")
def create_application(payload: DubaiFinanceApplicationCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.create"))):
    record = service.create_application(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Dubai finance application created")


@router.get("/applications/{application_id}")
def get_application(application_id: str, db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    record = service.get_application(db, user, application_id)
    return success_response(record, "Dubai finance application loaded")


@router.patch("/applications/{application_id}")
def update_application(application_id: str, payload: DubaiFinanceApplicationUpdate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.update_application(db, user, application_id, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "Dubai finance application updated")


@router.post("/applications/{application_id}/assign")
def assign_application(application_id: str, payload: DubaiFinanceAssignRequest, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.assign(db, user, application_id, payload.owner_id)
    db.commit()
    return success_response(record, "Dubai finance application assigned")


@router.post("/applications/{application_id}/upload-document")
def upload_document(application_id: str, payload: DubaiFinanceDocumentCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.upload_document(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Dubai finance document uploaded")


@router.post("/applications/{application_id}/eligibility-check")
def eligibility_check(application_id: str, payload: DubaiFinanceEligibilityRequest, db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    result = service.eligibility_check(db, user, application_id, payload.model_dump())
    db.commit()
    return success_response(result, "Eligibility checked")


@router.post("/applications/{application_id}/select-bank")
def select_bank(application_id: str, payload: DubaiFinanceBankSelectionCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.select_bank(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Bank selected")


@router.post("/applications/{application_id}/submit-to-bank")
def submit_to_bank(application_id: str, payload: DubaiFinanceBankSubmissionCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.submit_to_bank(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Submitted to bank")


@router.patch("/applications/{application_id}/bank-status")
def bank_status(application_id: str, payload: DubaiFinanceBankStatusUpdate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.update_bank_status(db, user, application_id, payload.model_dump())
    db.commit()
    return success_response(record, "Bank status updated")


@router.post("/applications/{application_id}/mark-approved")
def mark_approved(application_id: str, payload: DubaiFinanceDecisionRequest, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.mark_approved(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Application marked approved")


@router.post("/applications/{application_id}/mark-rejected")
def mark_rejected(application_id: str, payload: DubaiFinanceDecisionRequest, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.mark_rejected(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Application marked rejected")


@router.post("/applications/{application_id}/record-disbursal")
def record_disbursal(application_id: str, payload: DubaiFinanceDisbursalRequest, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    record = service.record_disbursal(db, user, application_id, payload.model_dump())
    db.commit()
    return success_response(record, "Disbursal recorded")


@router.post("/applications/{application_id}/record-commission")
def record_commission(application_id: str, payload: DubaiFinanceCommissionCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.payment"))):
    record = service.record_commission(db, user, application_id, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Commission recorded")


@router.get("/reports")
def reports(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    data, meta = service.reports(db, user)
    return success_response(data, "Dubai finance reports loaded", meta)
