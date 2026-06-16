from pydantic import BaseModel, EmailStr


class AdminUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: str | None = None
