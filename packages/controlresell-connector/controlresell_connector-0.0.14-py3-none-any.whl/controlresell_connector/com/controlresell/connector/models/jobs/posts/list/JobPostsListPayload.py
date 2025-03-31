from pydantic import BaseModel

class JobPostsListPayloadSchema(BaseModel):
    lastRetrieve: str | None
