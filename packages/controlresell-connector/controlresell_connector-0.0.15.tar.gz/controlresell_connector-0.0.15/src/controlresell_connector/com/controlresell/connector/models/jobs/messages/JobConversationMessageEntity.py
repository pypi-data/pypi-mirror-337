from pydantic import BaseModel
from typing import Optional

class JobConversationMessageEntity(BaseModel):
    body: Optional[str] = None
    photos: list[str]
    userId: str
    sentViaMobile: Optional[bool] = None
    id: str
    isHidden: Optional[bool] = None
