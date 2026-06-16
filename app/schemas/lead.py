from pydantic import BaseModel


class LeadCreate(BaseModel):
    full_name: str
    email: str | None = None
    mobile: str | None = None
    company: str | None = None
    source: str | None = None
    stage: str | None = "New"


class LeadUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    mobile: str | None = None
    company: str | None = None
    source: str | None = None
    stage: str | None = None


class LeadAssignRequest(BaseModel):
    owner_id: str


class LeadStageRequest(BaseModel):
    stage: str
