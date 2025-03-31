from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrderSchema

class JobConversationsGetPayloadSchema(BaseModel):
    accountId: UUID
    conversationId: str
    order: JobOrderSchema | None
