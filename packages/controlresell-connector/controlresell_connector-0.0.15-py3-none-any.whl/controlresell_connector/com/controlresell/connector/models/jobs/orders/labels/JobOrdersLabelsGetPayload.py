from pydantic import BaseModel
from uuid import UUID

class JobOrdersLabelsGetPayload(BaseModel):
    accountId: UUID
    platformId: str
    conversationId: str
    shipmentId: str
