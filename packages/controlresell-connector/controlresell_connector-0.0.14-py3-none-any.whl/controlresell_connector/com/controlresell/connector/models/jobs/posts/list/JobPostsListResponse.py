from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListedSchema

class JobPostsListResponseSchema(BaseModel):
    posts: list[JobPostListedSchema]
