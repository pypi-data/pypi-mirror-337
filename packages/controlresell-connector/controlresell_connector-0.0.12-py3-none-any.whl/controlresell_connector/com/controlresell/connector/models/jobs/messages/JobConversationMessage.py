from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessageEntityType import JobConversationMessageEntityTypeSchema
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessageEntity import JobConversationMessageEntitySchema
from datetime import datetime

class JobConversationMessageSchema(BaseModel):
    entityType: JobConversationMessageEntityTypeSchema
    entity: JobConversationMessageEntitySchema
    createdAtTs: datetime
    createdTimeAgo: str
