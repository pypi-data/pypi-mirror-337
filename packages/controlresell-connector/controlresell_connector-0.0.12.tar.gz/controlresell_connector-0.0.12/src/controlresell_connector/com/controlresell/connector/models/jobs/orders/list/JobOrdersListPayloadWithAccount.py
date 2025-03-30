from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobOrdersListPayloadWithAccountSchema(BaseModel):
    accountId: UUID
