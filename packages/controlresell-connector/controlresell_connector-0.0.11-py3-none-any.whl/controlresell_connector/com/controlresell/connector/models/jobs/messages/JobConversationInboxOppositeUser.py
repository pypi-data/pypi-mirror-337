from pydantic import BaseModel
from enum import Enum

class JobConversationInboxOppositeUserSchema(BaseModel):
    id: str
    login: str
    badge: str
