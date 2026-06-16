from app.models.support import Ticket
from app.repositories.base import BaseRepository


class TicketsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Ticket)
