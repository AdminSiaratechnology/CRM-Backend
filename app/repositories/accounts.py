from app.models.account import Account
from app.repositories.base import BaseRepository


class AccountsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Account)
