from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobPostsListPayloadWithAccountSchema(BaseModel):
    accountId: UUID
