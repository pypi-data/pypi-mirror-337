from pydantic import BaseModel
from uuid import UUID

class JobPostsListPayloadWithAccountSchema(BaseModel):
    accountId: UUID
