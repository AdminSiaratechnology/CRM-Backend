from app.models.finance import Invoice, Payment, Product, Quote
from app.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)


class QuotesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Quote)


class InvoicesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Invoice)


class PaymentsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Payment)
