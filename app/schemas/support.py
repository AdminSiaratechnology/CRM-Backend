from pydantic import BaseModel


class TicketCreate(BaseModel):
    subject: str
    priority: str | None = None
    description: str | None = None
