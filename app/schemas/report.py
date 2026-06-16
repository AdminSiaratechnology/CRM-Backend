from pydantic import BaseModel


class SavedReportCreate(BaseModel):
    name: str
