from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class Product(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(255), index=True)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)


class PriceBook(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "price_books"
    name: Mapped[str] = mapped_column(String(255), index=True)


class Quote(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "quotes"
    account_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    deal_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    total: Mapped[float | None] = mapped_column(Float, nullable=True)


class QuoteItem(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "quote_items"
    quote_id: Mapped[str] = mapped_column(String(36), index=True)
    product_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)


class Invoice(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "invoices"
    account_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    quote_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    total: Mapped[float | None] = mapped_column(Float, nullable=True)
    due_date: Mapped[str | None] = mapped_column(String(50), nullable=True)


class InvoiceItem(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "invoice_items"
    invoice_id: Mapped[str] = mapped_column(String(36), index=True)
    product_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)


class Payment(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "payments"
    invoice_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transaction_id: Mapped[str | None] = mapped_column(String(120), nullable=True)


class TaxRule(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "tax_rules"
    name: Mapped[str] = mapped_column(String(255), index=True)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)


class Proposal(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "proposals"
    title: Mapped[str] = mapped_column(String(255), index=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
