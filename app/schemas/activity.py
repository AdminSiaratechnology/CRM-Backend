from pydantic import BaseModel


class FollowUpCreate(BaseModel):
    related_module: str
    related_record_id: str
    due_at: str | None = None
    outcome: str | None = None
