from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.models.manager import Manager
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
