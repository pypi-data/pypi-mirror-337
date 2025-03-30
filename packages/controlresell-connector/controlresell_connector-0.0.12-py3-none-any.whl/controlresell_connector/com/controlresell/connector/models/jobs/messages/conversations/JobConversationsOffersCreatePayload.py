from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobConversationsOffersCreatePayloadSchema(BaseModel):
    accountId: UUID
    transactionId: str
    conversationId: str
    price: float
    currency: str
