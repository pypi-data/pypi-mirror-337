from pydantic import BaseModel
from uuid import UUID

class JobPostsDeleteResponse(BaseModel):
    accountId: UUID
    platformId: str
