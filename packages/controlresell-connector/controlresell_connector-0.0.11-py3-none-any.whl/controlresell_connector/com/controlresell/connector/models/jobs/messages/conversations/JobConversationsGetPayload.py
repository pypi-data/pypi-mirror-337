from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobConversationsGetPayloadSchema(BaseModel):
    accountId: UUID
    conversationId: str
