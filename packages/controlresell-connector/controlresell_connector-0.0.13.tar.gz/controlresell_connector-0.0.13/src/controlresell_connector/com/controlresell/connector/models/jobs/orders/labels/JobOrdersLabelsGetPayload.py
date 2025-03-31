from pydantic import BaseModel
from uuid import UUID

class JobOrdersLabelsGetPayloadSchema(BaseModel):
    accountId: UUID
    platformId: str
    conversationId: str
    shipmentId: str
