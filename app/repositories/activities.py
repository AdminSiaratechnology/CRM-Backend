from app.models.activity import FollowUp, Task, Meeting, Call
from app.repositories.base import BaseRepository


class TasksRepository(BaseRepository):
    def __init__(self):
        super().__init__(Task)


class MeetingsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Meeting)


class CallsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Call)


class FollowUpsRepository(BaseRepository):
    def __init__(self):
        super().__init__(FollowUp)
