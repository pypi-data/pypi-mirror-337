from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobOrdersLabelGetPayloadSchema(BaseModel):
    accountId: UUID
    platformId: str
    conversationId: str
    shipmentId: str
