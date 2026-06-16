from pydantic import BaseModel
from typing import Optional


class BranchBase(BaseModel):
    name: str
    code: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None


class BranchInDB(BranchBase):
    id: str

    class Config:
        from_attributes = True


class BranchResponse(BranchBase):
    id: str

    class Config:
        from_attributes = True