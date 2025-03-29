from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionalsSchema

class JobPostsUpdatePayloadSchema(BaseModel):
    accountId: UUID
    platformId: str
    post: JobPostOptionalsSchema
