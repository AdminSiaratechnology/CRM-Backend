from pydantic import BaseModel, EmailStr
from typing import List


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class CurrentUser(BaseModel):
    user_id: str
    tenant_id: str | None = None
    branch_id: str | None = None
    team_id: str | None = None
    role_name: str
    role_id: str | None = None
    scope: str = "OWN"
    permissions: List[str] = []
    is_superuser: bool = False

