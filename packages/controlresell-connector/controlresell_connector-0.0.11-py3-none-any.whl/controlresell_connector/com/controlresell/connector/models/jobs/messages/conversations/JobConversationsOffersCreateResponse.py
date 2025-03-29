from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobConversationsOffersCreateResponseSchema(BaseModel):
    accountId: UUID
    transactionId: str
