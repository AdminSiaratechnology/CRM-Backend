from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.user import User


class AuthService:
    def login(self, db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()
        if not user or not verify_password(password, user.password_hash):
            raise AppError("Invalid email or password", "INVALID_CREDENTIALS", 401)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "tenant_id": user.tenant_id,
                "role_id": user.role_id,
                "scope": user.scope,
            },
        }
