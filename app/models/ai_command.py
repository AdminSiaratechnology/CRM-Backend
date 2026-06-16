from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TenantScopedMixin, UUIDPrimaryKeyMixin


class AiAlert(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_alerts"
    severity: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    module: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    related_record_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    suggested_action: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiRecommendation(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_recommendations"
    title: Mapped[str] = mapped_column(String(255), index=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)


class AiRevenueLeak(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_revenue_leaks"
    title: Mapped[str] = mapped_column(String(255), index=True)
    amount_at_risk: Mapped[float | None] = mapped_column(Float, nullable=True)


class AiPrediction(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_predictions"
    prediction_type: Mapped[str] = mapped_column(String(120), index=True)
    predicted_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)


class AiCustomerHealth(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_customer_health"
    related_record_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiInsight(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_insights"
    title: Mapped[str] = mapped_column(String(255), index=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiRiskScore(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_risk_scores"
    related_record_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)


class AiExecutiveSummary(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_executive_summaries"
    period: Mapped[str] = mapped_column(String(50), index=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiDailyBriefing(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_daily_briefings"
    role_code: Mapped[str] = mapped_column(String(120), index=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiAutomationSuggestion(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_automation_suggestions"
    title: Mapped[str] = mapped_column(String(255), index=True)
    expected_impact: Mapped[str | None] = mapped_column(Text, nullable=True)


class AiEngineRun(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_engine_runs"
    engine_name: Mapped[str] = mapped_column(String(120), index=True)
    records_analyzed: Mapped[float | None] = mapped_column(Float, nullable=True)


class AiSettings(Base, UUIDPrimaryKeyMixin, TenantScopedMixin):
    __tablename__ = "ai_settings"
    llm_provider: Mapped[str | None] = mapped_column(String(120), nullable=True)
    settings_json: Mapped[str | None] = mapped_column(Text, nullable=True)
