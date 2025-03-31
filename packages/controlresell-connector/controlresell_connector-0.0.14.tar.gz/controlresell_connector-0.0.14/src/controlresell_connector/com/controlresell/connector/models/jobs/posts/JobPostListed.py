from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionalsSchema

class JobPostListedSchema(BaseModel):
    platformId: str
    platformUrl: str
    post: JobPostOptionalsSchema
    data: str
