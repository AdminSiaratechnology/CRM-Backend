from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    url: str | None = None
