from pydantic import BaseModel
from uuid import UUID

class JobOrdersLabelsGetResponseSchema(BaseModel):
    accountId: UUID
    platformId: str
    labelUrl: str
