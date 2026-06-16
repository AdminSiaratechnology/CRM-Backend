from sqlalchemy.orm import Session

from app.core.audit import write_audit_log
from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.dubai_finance import DubaiFinanceApplication
from app.repositories.dubai_finance import DubaiFinanceRepository
from app.schemas.auth import CurrentUser


WORKFLOW_STAGES = [
    "Application Created",
    "Telecaller Verified",
    "Documents Collected",
    "Eligibility Checked",
    "Bank Selected",
    "Coordinator Review",
    "Submitted to Bank",
    "Bank Under Review",
    "Additional Documents Required",
    "Approved",
    "Rejected",
    "Disbursed",
    "Commission Pending",
    "Commission Received",
    "Closed",
]


class DubaiFinanceService:
    def __init__(self):
        self.repository = DubaiFinanceRepository()

    def list_applications(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.repository.applications.list(db, scoped_filters(user), pagination)

    def get_application(self, db: Session, user: CurrentUser, application_id: str):
        return self.repository.applications.get(db, scoped_filters(user), application_id)

    def create_application(self, db: Session, user: CurrentUser, payload: dict):
        payload = {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id, "stage": payload.get("stage", "Application Created")}
        application = self.repository.applications.create(db, payload)
        self._write_history(db, user, application.id, None, application.stage, "Application created")
        write_audit_log(db, tenant_id=user.tenant_id, actor_id=user.user_id, module="dubai_finance", action="create", entity_id=application.id, after_data={"stage": application.stage})
        return application

    def update_application(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        application = self.get_application(db, user, application_id)
        previous_stage = application.stage
        updated = self.repository.applications.update(db, application, {**payload, "updated_by_id": user.user_id})
        if payload.get("stage") and payload.get("stage") != previous_stage:
            self._write_history(db, user, application_id, previous_stage, payload["stage"], payload.get("notes") or "Stage updated")
        return updated

    def assign(self, db: Session, user: CurrentUser, application_id: str, owner_id: str):
        application = self.get_application(db, user, application_id)
        return self.repository.applications.update(db, application, {"owner_id": owner_id, "updated_by_id": user.user_id})

    def upload_document(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        document = self.repository.documents.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id})
        self._advance_stage(db, user, application_id, "Documents Collected", "Document uploaded")
        return document

    def eligibility_check(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        application = self.get_application(db, user, application_id)
        monthly_income = float(payload.get("monthly_income") or 0)
        requested_amount = float(payload.get("requested_amount") or application.required_amount or 0)
        property_value = float(payload.get("property_value") or 0)
        tenure_months = int(payload.get("tenure_months") or 0)
        income_ok = monthly_income >= (requested_amount / max(tenure_months, 1) / 3 if tenure_months else requested_amount * 0.03)
        ltv_ok = not property_value or requested_amount <= property_value * 0.8
        verdict = "Eligible" if income_ok and ltv_ok else "Review Required"
        self._write_history(db, user, application_id, application.stage, "Eligibility Checked", verdict)
        application.stage = "Eligibility Checked"
        return {"application_id": application_id, "verdict": verdict, "income_ok": income_ok, "ltv_ok": ltv_ok}

    def select_bank(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        record = self.repository.bank_selections.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id})
        self._advance_stage(db, user, application_id, "Bank Selected", f"Selected bank {payload.get('bank_name')}")
        return record

    def submit_to_bank(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        record = self.repository.bank_submissions.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id, "bank_status": payload.get("bank_status", "Submitted")})
        self._advance_stage(db, user, application_id, "Submitted to Bank", f"Submitted to bank {payload.get('bank_name')}")
        return record

    def update_bank_status(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        rows, _ = self.repository.bank_submissions.list(db, {**scoped_filters(user), "application_id": application_id}, PaginationParams(page=1, limit=20))
        record = rows[0] if rows else self.repository.bank_submissions.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id})
        return self.repository.bank_submissions.update(db, record, {**payload, "updated_by_id": user.user_id})

    def mark_approved(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        record = self.repository.approvals.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id, "decision": "Approved"})
        self._advance_stage(db, user, application_id, "Approved", payload.get("remarks") or "Bank approved")
        return record

    def mark_rejected(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        record = self.repository.approvals.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id, "decision": "Rejected"})
        self._advance_stage(db, user, application_id, "Rejected", payload.get("remarks") or "Bank rejected")
        return record

    def record_disbursal(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        application = self.get_application(db, user, application_id)
        updated = self.repository.applications.update(db, application, {"approved_amount": payload.get("approved_amount", application.approved_amount), "stage": "Disbursed", "updated_by_id": user.user_id})
        self._write_history(db, user, application_id, application.stage, "Disbursed", payload.get("remarks") or "Disbursed")
        return updated

    def record_commission(self, db: Session, user: CurrentUser, application_id: str, payload: dict):
        commission = self.repository.commissions.create(db, {**payload, **scoped_filters(user), "application_id": application_id, "created_by_id": user.user_id, "updated_by_id": user.user_id, "commission_status": payload.get("commission_status", "Pending")})
        self._advance_stage(db, user, application_id, "Commission Pending", "Commission record created")
        return commission

    def reports(self, db: Session, user: CurrentUser):
        rows, meta = self.repository.applications.list(db, scoped_filters(user), PaginationParams(page=1, limit=200))
        summary = {"total_applications": meta["total"], "by_stage": {}, "applications": rows, "workflow": WORKFLOW_STAGES}
        for row in rows:
            summary["by_stage"][row.stage] = summary["by_stage"].get(row.stage, 0) + 1
        return summary, meta

    def _write_history(self, db: Session, user: CurrentUser, application_id: str, from_stage: str | None, to_stage: str, reason: str):
        self.repository.status_history.create(db, {**scoped_filters(user), "application_id": application_id, "from_stage": from_stage, "to_stage": to_stage, "reason": reason, "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def _advance_stage(self, db: Session, user: CurrentUser, application_id: str, to_stage: str, reason: str):
        application = self.get_application(db, user, application_id)
        previous_stage = application.stage
        self.repository.applications.update(db, application, {"stage": to_stage, "updated_by_id": user.user_id})
        self._write_history(db, user, application_id, previous_stage, to_stage, reason)
