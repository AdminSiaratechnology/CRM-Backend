from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class PermissionBase(BaseModel):
    module: str
    action: str
    name: Optional[str] = None
    code: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "active"


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    module: Optional[str] = None
    action: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class PermissionResponse(BaseModel):
    id: str
    tenant_id: Optional[str]
    module: str
    action: str
    name: str
    code: str
    label: str
    description: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ModulePermissions(BaseModel):
    module: str
    permissions: List[PermissionResponse]


class RolePermissionsUpdate(BaseModel):
    permission_ids: List[str]


class RolePermissionsResponse(BaseModel):
    assigned_permission_ids: List[str]
    all_permissions: List[ModulePermissions]


class UserPermissionsResponse(BaseModel):
    permissions: List[str]
