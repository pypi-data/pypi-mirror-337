from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobOrdersLabelGetResponseSchema(BaseModel):
    accountId: UUID
    platformId: str
    labelUrl: str
