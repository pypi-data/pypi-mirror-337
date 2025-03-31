from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.JobConversation import JobConversationSchema
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrderSchema

class JobConversationsGetResponseSchema(BaseModel):
    conversation: JobConversationSchema
    order: JobOrderSchema | None
