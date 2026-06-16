from pydantic import BaseModel


class RunEngineRequest(BaseModel):
    trigger: str = "manual"
