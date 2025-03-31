from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessageEntityType import JobConversationMessageEntityType
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessageEntity import JobConversationMessageEntity
from datetime import datetime

class JobConversationMessage(BaseModel):
    entityType: JobConversationMessageEntityType
    entity: JobConversationMessageEntity
    createdAtTs: datetime
    createdTimeAgo: str
