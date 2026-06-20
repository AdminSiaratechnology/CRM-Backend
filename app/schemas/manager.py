from pydantic import BaseModel
from typing import Optional


class ManagerBase(BaseModel):
    name: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[str] = None


class ManagerCreate(ManagerBase):
    pass


class ManagerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[str] = None


class ManagerInDB(ManagerBase):
    id: str

    class Config:
        from_attributes = True


class ManagerResponse(ManagerBase):
    id: str

    class Config:
        from_attributes = True
