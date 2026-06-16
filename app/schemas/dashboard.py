from pydantic import BaseModel


class DashboardFilter(BaseModel):
    branch_id: str | None = None
    team_id: str | None = None
    date_from: str | None = None
    date_to: str | None = None
