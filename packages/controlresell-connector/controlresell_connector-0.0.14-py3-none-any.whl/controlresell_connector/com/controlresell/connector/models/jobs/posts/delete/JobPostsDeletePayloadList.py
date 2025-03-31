from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.delete.JobPostsDeletePayload import JobPostsDeletePayloadSchema

class JobPostsDeletePayloadListSchema(BaseModel):
    payloads: list[JobPostsDeletePayloadSchema]
