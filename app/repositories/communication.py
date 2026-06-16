from app.models.communication import CommunicationLog, CommunicationSetting, CommunicationTemplate
from app.repositories.base import BaseRepository


class CommunicationSettingsRepository(BaseRepository):
    def __init__(self):
        super().__init__(CommunicationSetting)


class CommunicationLogsRepository(BaseRepository):
    def __init__(self):
        super().__init__(CommunicationLog)


class CommunicationTemplatesRepository(BaseRepository):
    def __init__(self):
        super().__init__(CommunicationTemplate)
