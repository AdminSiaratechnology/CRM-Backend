from pydantic import BaseModel


class ContactCreate(BaseModel):
    full_name: str
    email: str | None = None
    mobile: str | None = None
