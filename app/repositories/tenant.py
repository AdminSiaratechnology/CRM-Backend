from app.models.tenant import Tenant
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository):
    def __init__(self):
        super().__init__(Tenant)
