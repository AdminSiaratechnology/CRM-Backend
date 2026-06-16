from pydantic import BaseModel


class AccountCreate(BaseModel):
    company_name: str
    industry: str | None = None
