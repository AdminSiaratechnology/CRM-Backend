from pydantic import BaseModel
from typing import Optional


class RoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    data_access_level: Optional[str] = None  # Tenant, Country, Region, Branch, Team, Own records
    permissions_matrix: Optional[str] = None
    status: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    data_access_level: Optional[str] = None
    permissions_matrix: Optional[str] = None
    status: Optional[str] = None


class RoleInDB(RoleBase):
    id: str

    class Config:
        from_attributes = True


class RoleResponse(RoleBase):
    id: str

    class Config:
        from_attributes = True
