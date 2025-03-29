from pydantic import BaseModel
from enum import Enum

class JobPostsListPayloadSchema(BaseModel):
    lastRetrieve: str | None
