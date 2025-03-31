from pydantic import BaseModel
from uuid import UUID

class JobOrdersListPayloadWithAccountSchema(BaseModel):
    accountId: UUID
