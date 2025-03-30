from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionalsSchema

class JobPostListedSchema(BaseModel):
    platformId: str
    platformUrl: str
    post: JobPostOptionalsSchema
    data: str
