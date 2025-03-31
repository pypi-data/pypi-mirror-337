from pydantic import BaseModel
from datetime import datetime
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobConversationInboxOppositeUser import JobConversationInboxOppositeUser

class JobInboxConversation(BaseModel):
    conversationId: str
    itemCount: int
    isDeletionRestricted: bool
    description: str
    unread: bool
    updatedAt: datetime
    oppositeUser: JobConversationInboxOppositeUser
