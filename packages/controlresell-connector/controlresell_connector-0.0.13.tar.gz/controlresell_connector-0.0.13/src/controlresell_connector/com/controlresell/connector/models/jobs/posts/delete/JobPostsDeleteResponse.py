from pydantic import BaseModel
from uuid import UUID

class JobPostsDeleteResponseSchema(BaseModel):
    accountId: UUID
    platformId: str
