from app.models.integration import IntegrationConnection, IntegrationCredential, IntegrationLog
from app.repositories.base import BaseRepository


class IntegrationConnectionsRepository(BaseRepository):
    def __init__(self):
        super().__init__(IntegrationConnection)


class IntegrationCredentialsRepository(BaseRepository):
    def __init__(self):
        super().__init__(IntegrationCredential)


class IntegrationLogsRepository(BaseRepository):
    def __init__(self):
        super().__init__(IntegrationLog)
