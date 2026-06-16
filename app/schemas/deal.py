from pydantic import BaseModel


class DealCreate(BaseModel):
    name: str
    account_id: str | None = None
    contact_id: str | None = None
    stage: str | None = "New Opportunity"
    value: float | None = None
    probability: float | None = None


class DealStageRequest(BaseModel):
    stage: str
