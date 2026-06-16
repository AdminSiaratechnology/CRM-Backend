from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class DubaiFinanceApplication(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_applications"
    application_number: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    applicant_name: Mapped[str] = mapped_column(String(255), index=True)
    applicant_mobile: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    applicant_email: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    stage: Mapped[str] = mapped_column(String(100), index=True, default="Application Created")
    required_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    approved_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class DubaiFinanceApplicant(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_applicants"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    mobile: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(120), nullable=True)


class DubaiFinanceEmployment(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_employments"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    employer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    monthly_income: Mapped[float | None] = mapped_column(Float, nullable=True)


class DubaiFinanceRequirement(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_requirements"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    requirement_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    property_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    requested_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    tenure_months: Mapped[int | None] = mapped_column(Integer, nullable=True)


class DubaiFinanceDocument(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_documents"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    document_type: Mapped[str] = mapped_column(String(120), index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(80), index=True, default="Collected")


class DubaiFinanceBankSelection(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_bank_selections"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    bank_name: Mapped[str] = mapped_column(String(120), index=True)
    selected_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)


class DubaiFinanceBankSubmission(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_bank_submissions"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    bank_name: Mapped[str] = mapped_column(String(120), index=True)
    submission_reference: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    bank_status: Mapped[str] = mapped_column(String(120), index=True, default="Submitted")
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)


class DubaiFinanceStatusHistory(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_status_history"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    from_stage: Mapped[str | None] = mapped_column(String(100), nullable=True)
    to_stage: Mapped[str] = mapped_column(String(100), index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class DubaiFinanceApprovalRejection(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_approval_rejections"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    decision: Mapped[str] = mapped_column(String(50), index=True)
    decided_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)


class DubaiFinanceCommission(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "dubai_finance_commissions"
    application_id: Mapped[str] = mapped_column(String(36), index=True)
    bank_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission_status: Mapped[str] = mapped_column(String(80), index=True, default="Pending")
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
