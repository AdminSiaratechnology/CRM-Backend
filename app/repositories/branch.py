from app.models.branch import Branch
from app.repositories.base import BaseRepository


class BranchRepository(BaseRepository):
    def __init__(self):
        super().__init__(Branch)
