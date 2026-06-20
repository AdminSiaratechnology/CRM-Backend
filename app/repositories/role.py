from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Role)
