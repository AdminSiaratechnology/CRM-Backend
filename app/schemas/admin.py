from pydantic import BaseModel, EmailStr


class RelatedEntity(BaseModel):
    """Schema for related entities (role, branch, manager) with id and name."""
    id: str
    name: str
    
    class Config:
        from_attributes = True


class AdminUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str | None = None
    role_id: str | None = None
    branch_id: str | None = None
    manager_id: str | None = None
    status: str = "active"
    login_access: bool = True
    gps_access: bool = False
    monthly_target: int | None = None
    agency_name: str | None = None
    is_superuser: bool = False
    superuser_privileges: bool | None = None
    permissions: list[str] | None = None
    permissions_matrix: dict | str | None = None


class AdminUserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    mobile: str | None = None
    role_id: str | None = None
    branch_id: str | None = None
    manager_id: str | None = None
    status: str | None = None
    login_access: bool | None = None
    gps_access: bool | None = None
    monthly_target: int | None = None
    agency_name: str | None = None
    is_superuser: bool | None = None
    superuser_privileges: bool | None = None
    permissions: list[str] | None = None
    permissions_matrix: dict | str | None = None


class AdminUserResponse(BaseModel):
    """Response schema for user with related entity details."""
    id: str
    name: str
    email: str
    mobile: str | None = None
    status: str | None = None
    login_access: bool
    gps_access: bool
    monthly_target: int | None = None
    role_id: str | None = None
    branch_id: str | None = None
    manager_id: str | None = None
    role: RelatedEntity | None = None
    branch: RelatedEntity | None = None
    manager: RelatedEntity | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by_id: str | None = None
    updated_by_id: str | None = None
    agency_name: str | None = None
    is_superuser: bool = False
    permissions_matrix: dict | str | None = None
    
    class Config:
        from_attributes = True
