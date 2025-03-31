from pydantic import BaseModel

class JobConversationInboxOppositeUserSchema(BaseModel):
    id: str
    login: str
    badge: str
