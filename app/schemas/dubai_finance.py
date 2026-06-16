from pydantic import BaseModel, Field


class DubaiFinanceApplicationCreate(BaseModel):
    application_number: str
    applicant_name: str
    applicant_mobile: str | None = None
    applicant_email: str | None = None
    employment_type: str | None = None
    bank_name: str | None = None
    required_amount: float | None = None
    notes: str | None = None


class DubaiFinanceApplicationUpdate(BaseModel):
    application_number: str | None = None
    applicant_name: str | None = None
    applicant_mobile: str | None = None
    applicant_email: str | None = None
    employment_type: str | None = None
    bank_name: str | None = None
    stage: str | None = None
    required_amount: float | None = None
    approved_amount: float | None = None
    notes: str | None = None


class DubaiFinanceAssignRequest(BaseModel):
    owner_id: str


class DubaiFinanceDocumentCreate(BaseModel):
    document_type: str
    file_name: str
    file_url: str | None = None


class DubaiFinanceEligibilityRequest(BaseModel):
    monthly_income: float | None = None
    requested_amount: float | None = None
    property_value: float | None = None
    tenure_months: int | None = Field(default=None, ge=1)


class DubaiFinanceBankSelectionCreate(BaseModel):
    bank_name: str
    selected_by: str | None = None
    remarks: str | None = None


class DubaiFinanceBankSubmissionCreate(BaseModel):
    bank_name: str
    submission_reference: str | None = None
    bank_status: str | None = "Submitted"
    remarks: str | None = None


class DubaiFinanceBankStatusUpdate(BaseModel):
    bank_status: str
    remarks: str | None = None


class DubaiFinanceDecisionRequest(BaseModel):
    decision: str
    decided_by: str | None = None
    remarks: str | None = None


class DubaiFinanceDisbursalRequest(BaseModel):
    approved_amount: float | None = None
    remarks: str | None = None


class DubaiFinanceCommissionCreate(BaseModel):
    bank_name: str | None = None
    amount: float | None = None
    commission_status: str | None = "Pending"
    remarks: str | None = None
