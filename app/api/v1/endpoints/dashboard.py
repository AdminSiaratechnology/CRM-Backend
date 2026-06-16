from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import success_response
from app.middleware.auth_middleware import get_current_user, require_permission
from app.services.dashboard_service import DashboardService

router = APIRouter()
service = DashboardService()


@router.get("/executive")
def executive(db: Session = Depends(get_db), user=Depends(require_permission("reports.view"))):
    return success_response(service.executive(db, user), "Executive dashboard loaded")
