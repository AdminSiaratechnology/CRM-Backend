from pydantic import BaseModel


class CommunicationSendRequest(BaseModel):
    recipient: str
    body: str
