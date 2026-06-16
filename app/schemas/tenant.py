from pydantic import BaseModel
from datetime import datetime


class TenantBase(BaseModel):
    name: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
