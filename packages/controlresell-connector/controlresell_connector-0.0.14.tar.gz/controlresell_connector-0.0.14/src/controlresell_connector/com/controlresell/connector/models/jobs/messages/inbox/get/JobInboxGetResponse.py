from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobInboxConversation import JobInboxConversationSchema

class JobInboxGetResponseSchema(BaseModel):
    conversations: list[JobInboxConversationSchema]
