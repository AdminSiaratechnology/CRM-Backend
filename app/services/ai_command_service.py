from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.tenant import scoped_filters
from app.repositories.ai_command import AiAlertsRepository, AiCustomerHealthRepository, AiPredictionsRepository, AiRecommendationsRepository, AiRevenueLeaksRepository
from app.schemas.auth import CurrentUser


class AiCommandService:
    def __init__(self):
        self.alerts = AiAlertsRepository()
        self.recommendations = AiRecommendationsRepository()
        self.revenue_leaks = AiRevenueLeaksRepository()
        self.predictions = AiPredictionsRepository()
        self.customer_health = AiCustomerHealthRepository()

    def dashboard(self, db: Session, user: CurrentUser):
        filters = scoped_filters(user)
        alerts, _ = self.alerts.list(db, filters, PaginationParams(page=1, limit=10))
        revenue_leaks, _ = self.revenue_leaks.list(db, filters, PaginationParams(page=1, limit=10))
        predictions, _ = self.predictions.list(db, filters, PaginationParams(page=1, limit=10))
        return {"alerts": alerts, "revenue_leaks": revenue_leaks, "predictions": predictions}

    def list_alerts(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.alerts.list(db, scoped_filters(user), pagination)

    def list_recommendations(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.recommendations.list(db, scoped_filters(user), pagination)

    def list_revenue_leaks(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.revenue_leaks.list(db, scoped_filters(user), pagination)

    def list_predictions(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.predictions.list(db, scoped_filters(user), pagination)

    def list_customer_health(self, db: Session, user: CurrentUser, pagination: PaginationParams):
        return self.customer_health.list(db, scoped_filters(user), pagination)

    def run(self, db: Session, user: CurrentUser, trigger: str):
        return {"trigger": trigger, "status": "queued", "tenant_id": user.tenant_id}
