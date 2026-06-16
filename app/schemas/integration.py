from pydantic import BaseModel


class IntegrationCreate(BaseModel):
    provider: str
