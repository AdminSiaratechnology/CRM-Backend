from app.models.manager import Manager
from app.repositories.base import BaseRepository


class ManagerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Manager)
