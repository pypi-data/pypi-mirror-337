from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionals

class JobPostListed(BaseModel):
    platformId: str
    platformUrl: str
    post: JobPostOptionals
    data: str
