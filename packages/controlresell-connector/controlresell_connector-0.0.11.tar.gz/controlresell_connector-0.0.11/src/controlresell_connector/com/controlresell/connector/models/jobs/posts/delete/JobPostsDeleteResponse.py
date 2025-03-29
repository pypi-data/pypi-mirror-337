from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobPostsDeleteResponseSchema(BaseModel):
    accountId: UUID
    platformId: str
