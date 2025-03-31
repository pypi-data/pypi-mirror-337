from pydantic import BaseModel
from uuid import UUID

class JobConversationsOffersCreatePayloadSchema(BaseModel):
    accountId: UUID
    transactionId: str
    conversationId: str
    price: float
    currency: str
