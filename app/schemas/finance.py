from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    sku: str | None = None
    price: float | None = None


class QuoteCreate(BaseModel):
    account_id: str | None = None
    deal_id: str | None = None
    total: float | None = None


class PaymentCreate(BaseModel):
    invoice_id: str | None = None
    amount: float
    method: str | None = None
