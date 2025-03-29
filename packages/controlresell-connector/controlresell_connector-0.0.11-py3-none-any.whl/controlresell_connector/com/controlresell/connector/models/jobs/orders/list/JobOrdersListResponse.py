from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListedSchema

class JobOrdersListResponseSchema(BaseModel):
    orders: JobPostListedSchema
