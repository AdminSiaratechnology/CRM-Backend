from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=200)
    search: str | None = None
    sort_by: str | None = None
    sort_dir: str = "desc"

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
