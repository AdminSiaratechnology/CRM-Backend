from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.middleware.auth_middleware import get_current_user
from app.schemas.auth import LoginRequest, RefreshRequest
from app.services.auth_service import AuthService

router = APIRouter()
service = AuthService()


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return success_response(service.login(db, payload.email, payload.password), "Login successful")


@router.post("/logout")
def logout():
    return success_response({"logged_out": True}, "Logout successful")


@router.get("/me")
def me(user=Depends(get_current_user)):
    return success_response(user.model_dump(), "Current user loaded")


@router.post("/refresh")
def refresh(_: RefreshRequest):
    return success_response({"refreshed": True}, "Refresh handled")
