from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobInboxConversation import JobInboxConversationSchema

class JobInboxGetResponseSchema(BaseModel):
    conversations: JobInboxConversationSchema
