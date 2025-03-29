from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.posts.delete.JobPostsDeletePayload import JobPostsDeletePayloadSchema

class JobPostsDeletePayloadListSchema(BaseModel):
    payloads: JobPostsDeletePayloadSchema
