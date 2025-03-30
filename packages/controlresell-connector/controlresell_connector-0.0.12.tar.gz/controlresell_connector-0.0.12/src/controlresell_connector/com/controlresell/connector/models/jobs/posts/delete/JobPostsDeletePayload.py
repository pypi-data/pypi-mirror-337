from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobPostsDeletePayloadSchema(BaseModel):
    accountId: UUID
    platformId: str
