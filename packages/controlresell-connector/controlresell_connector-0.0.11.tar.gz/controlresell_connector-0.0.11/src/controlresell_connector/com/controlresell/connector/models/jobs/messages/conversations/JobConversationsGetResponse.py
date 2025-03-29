from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversation import JobConversationSchema

class JobConversationsGetResponseSchema(BaseModel):
    conversation: JobConversationSchema
