from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.models.finance import Invoice
from app.repositories.finance import InvoicesRepository, PaymentsRepository, ProductsRepository, QuotesRepository
from app.schemas.auth import CurrentUser


class FinanceService:
    def __init__(self):
        self.products = ProductsRepository()
        self.quotes = QuotesRepository()
        self.invoices = InvoicesRepository()
        self.payments = PaymentsRepository()

    def list_products(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.products.list(db, scoped_filters(user), pagination)

    def create_product(self, db: Session, user: CurrentUser, payload: dict):
        return self.products.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id})

    def list_quotes(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.quotes.list(db, scoped_filters(user), pagination)

    def create_quote(self, db: Session, user: CurrentUser, payload: dict):
        return self.quotes.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id, "status": "Draft"})

    def convert_quote_to_invoice(self, db: Session, user: CurrentUser, quote_id: str):
        quote = self.quotes.get(db, scoped_filters(user), quote_id)
        invoice = Invoice(tenant_id=user.tenant_id, branch_id=quote.branch_id, team_id=quote.team_id, owner_id=quote.owner_id, created_by_id=user.user_id, updated_by_id=user.user_id, account_id=quote.account_id, quote_id=quote.id, total=quote.total, status="Unpaid")
        db.add(invoice)
        quote.status = "Converted to Invoice"
        db.flush()
        return invoice

    def list_invoices(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.invoices.list(db, scoped_filters(user), pagination)

    def create_invoice(self, db: Session, user: CurrentUser, payload: dict):
        return self.invoices.create(db, {**payload, **scoped_filters(user), "created_by_id": user.user_id, "updated_by_id": user.user_id, "status": payload.get("status", "Unpaid")})

    def record_payment(self, db: Session, user: CurrentUser, invoice_id: str, payload: dict):
        payment = self.payments.create(db, {**payload, **scoped_filters(user), "invoice_id": invoice_id, "created_by_id": user.user_id, "updated_by_id": user.user_id, "status": "Paid"})
        invoice = self.invoices.get(db, scoped_filters(user), invoice_id)
        if invoice:
            invoice.status = "Paid"
        return payment

    def list_payments(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.payments.list(db, scoped_filters(user), pagination)
