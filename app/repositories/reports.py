from app.models.report import DashboardWidget, SavedReport
from app.repositories.base import BaseRepository


class SavedReportsRepository(BaseRepository):
    def __init__(self):
        super().__init__(SavedReport)


class DashboardWidgetsRepository(BaseRepository):
    def __init__(self):
        super().__init__(DashboardWidget)
