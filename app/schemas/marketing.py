from pydantic import BaseModel


class CampaignCreate(BaseModel):
    name: str
    channel: str | None = None
