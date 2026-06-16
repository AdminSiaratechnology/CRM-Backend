from app.models.marketing import Campaign, LandingPage, LeadForm, Segment
from app.repositories.base import BaseRepository


class CampaignsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Campaign)


class SegmentsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Segment)


class LeadFormsRepository(BaseRepository):
    def __init__(self):
        super().__init__(LeadForm)


class LandingPagesRepository(BaseRepository):
    def __init__(self):
        super().__init__(LandingPage)
