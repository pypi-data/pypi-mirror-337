from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversation import JobConversationSchema
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrderSchema

class JobConversationsGetResponseSchema(BaseModel):
    conversation: JobConversationSchema
    order: JobOrderSchema | None
