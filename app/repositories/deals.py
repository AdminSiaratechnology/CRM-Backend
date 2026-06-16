from app.models.deal import Deal
from app.repositories.base import BaseRepository


class DealsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Deal)
