from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Document)
