from pydantic import BaseModel
from enum import Enum
from zodable_idschema import IdSchema
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPost import JobPostSchema

class JobPostsCreatePayloadSchema(BaseModel):
    itemId: IdSchema
    post: JobPostSchema
