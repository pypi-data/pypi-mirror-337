from pydantic import BaseModel
from datetime import datetime
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobConversationInboxOppositeUser import JobConversationInboxOppositeUserSchema

class JobInboxConversationSchema(BaseModel):
    conversationId: str
    itemCount: int
    isDeletionRestricted: bool
    description: str
    unread: bool
    updatedAt: datetime
    oppositeUser: JobConversationInboxOppositeUserSchema
