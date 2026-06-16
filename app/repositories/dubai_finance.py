from app.models.dubai_finance import (
    DubaiFinanceApplicant,
    DubaiFinanceApplication,
    DubaiFinanceApprovalRejection,
    DubaiFinanceBankSelection,
    DubaiFinanceBankSubmission,
    DubaiFinanceCommission,
    DubaiFinanceDocument,
    DubaiFinanceEmployment,
    DubaiFinanceRequirement,
    DubaiFinanceStatusHistory,
)
from app.repositories.base import BaseRepository


class DubaiFinanceRepository:
    def __init__(self):
        self.applications = BaseRepository(DubaiFinanceApplication)
        self.applicants = BaseRepository(DubaiFinanceApplicant)
        self.employments = BaseRepository(DubaiFinanceEmployment)
        self.requirements = BaseRepository(DubaiFinanceRequirement)
        self.documents = BaseRepository(DubaiFinanceDocument)
        self.bank_selections = BaseRepository(DubaiFinanceBankSelection)
        self.bank_submissions = BaseRepository(DubaiFinanceBankSubmission)
        self.status_history = BaseRepository(DubaiFinanceStatusHistory)
        self.approvals = BaseRepository(DubaiFinanceApprovalRejection)
        self.commissions = BaseRepository(DubaiFinanceCommission)
