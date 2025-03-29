from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class JobConversationMessageSchema(BaseModel):
    body: str
    userId: int
    sentViaMobile: bool
    messageId: int
    reaction: str | None
    isHidden: bool | None
    createdAt: datetime
    createdTimeAgo: str | None
