from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.core.pagination import PaginationParams
from app.middleware.auth_middleware import require_permission
from app.schemas.finance import PaymentCreate, ProductCreate, QuoteCreate
from app.services.finance_service import FinanceService

router = APIRouter()
service = FinanceService()


@router.get("/products")
def list_products(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    rows, meta = service.list_products(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Products loaded", meta)


@router.post("/products")
def create_product(payload: ProductCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.create"))):
    record = service.create_product(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Product created")


@router.get("/quotes")
def list_quotes(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    rows, meta = service.list_quotes(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Quotes loaded", meta)


@router.post("/quotes")
def create_quote(payload: QuoteCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.create"))):
    record = service.create_quote(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Quote created")


@router.patch("/quotes/{quote_id}")
def update_quote(quote_id: str, payload: QuoteCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.edit"))):
    quote = service.quotes.get(db, {"tenant_id": user.tenant_id, "deleted_at": None}, quote_id)
    record = service.quotes.update(db, quote, payload.model_dump(exclude_none=True))
    db.commit()
    return success_response(record, "Quote updated")


@router.post("/quotes/{quote_id}/convert-to-invoice")
def convert_quote_to_invoice(quote_id: str, db: Session = Depends(get_db), user=Depends(require_permission("finance.create"))):
    invoice = service.convert_quote_to_invoice(db, user, quote_id)
    db.commit()
    db.refresh(invoice)
    return success_response(invoice, "Quote converted to invoice")


@router.get("/invoices")
def list_invoices(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    rows, meta = service.list_invoices(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Invoices loaded", meta)


@router.post("/invoices")
def create_invoice(payload: QuoteCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.create"))):
    record = service.create_invoice(db, user, payload.model_dump())
    db.commit()
    db.refresh(record)
    return success_response(record, "Invoice created")


@router.post("/invoices/{invoice_id}/record-payment")
def record_payment(invoice_id: str, payload: PaymentCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.payment"))):
    payment = service.record_payment(db, user, invoice_id, payload.model_dump())
    db.commit()
    db.refresh(payment)
    return success_response(payment, "Payment recorded")


@router.get("/payments")
def list_payments(page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db), user=Depends(require_permission("finance.view"))):
    rows, meta = service.list_payments(db, user, PaginationParams(page=page, limit=limit))
    return success_response(rows, "Payments loaded", meta)


@router.post("/payments")
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db), user=Depends(require_permission("finance.payment"))):
    payment = service.payments.create(db, {**payload.model_dump(), "tenant_id": user.tenant_id, "created_by_id": user.user_id, "updated_by_id": user.user_id})
    db.commit()
    db.refresh(payment)
    return success_response(payment, "Payment created")


@router.get("/reports")
def finance_reports(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    rows, meta = service.list_invoices(db, user, PaginationParams(page=1, limit=50))
    return success_response({"rows": rows}, "Finance reports loaded", meta)
