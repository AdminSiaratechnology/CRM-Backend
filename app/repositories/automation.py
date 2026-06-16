from app.models.automation import AssignmentRule, ReminderRule, WebhookEndpoint, Workflow, WorkflowRun
from app.repositories.base import BaseRepository


class WorkflowsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Workflow)


class WorkflowRunsRepository(BaseRepository):
    def __init__(self):
        super().__init__(WorkflowRun)


class AssignmentRulesRepository(BaseRepository):
    def __init__(self):
        super().__init__(AssignmentRule)


class ReminderRulesRepository(BaseRepository):
    def __init__(self):
        super().__init__(ReminderRule)


class WebhookEndpointsRepository(BaseRepository):
    def __init__(self):
        super().__init__(WebhookEndpoint)
