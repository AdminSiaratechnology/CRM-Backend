from app.models.ai_command import AiAlert, AiRecommendation, AiRevenueLeak, AiPrediction, AiCustomerHealth
from app.repositories.base import BaseRepository


class AiAlertsRepository(BaseRepository):
    def __init__(self):
        super().__init__(AiAlert)


class AiRecommendationsRepository(BaseRepository):
    def __init__(self):
        super().__init__(AiRecommendation)


class AiRevenueLeaksRepository(BaseRepository):
    def __init__(self):
        super().__init__(AiRevenueLeak)


class AiPredictionsRepository(BaseRepository):
    def __init__(self):
        super().__init__(AiPrediction)


class AiCustomerHealthRepository(BaseRepository):
    def __init__(self):
        super().__init__(AiCustomerHealth)
