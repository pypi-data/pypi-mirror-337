from pydantic import BaseModel
from uuid import UUID

class JobPostsDeletePayloadSchema(BaseModel):
    accountId: UUID
    platformId: str
