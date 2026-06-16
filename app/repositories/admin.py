from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)


class RolesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Role)


class PermissionsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Permission)
