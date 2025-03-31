from pydantic import BaseModel
from uuid import UUID

class JobInboxGetPayloadSchema(BaseModel):
    accountId: UUID
