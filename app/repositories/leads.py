from app.models.lead import Lead
from app.repositories.base import BaseRepository


class LeadsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Lead)
