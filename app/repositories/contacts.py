from app.models.contact import Contact
from app.repositories.base import BaseRepository


class ContactsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Contact)
