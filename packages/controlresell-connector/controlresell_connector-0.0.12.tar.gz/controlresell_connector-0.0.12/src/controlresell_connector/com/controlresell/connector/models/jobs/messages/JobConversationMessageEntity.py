from pydantic import BaseModel
from enum import Enum

class JobConversationMessageEntitySchema(BaseModel):
    body: str | None
    photos: str
    userId: str
    sentViaMobile: bool | None
    id: str
    isHidden: bool | None
