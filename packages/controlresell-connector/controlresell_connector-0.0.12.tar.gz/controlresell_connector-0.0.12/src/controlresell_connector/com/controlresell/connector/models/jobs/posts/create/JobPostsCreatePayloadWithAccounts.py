from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.posts.create.JobPostsCreatePayload import JobPostsCreatePayloadSchema

class JobPostsCreatePayloadWithAccountsSchema(BaseModel):
    accountsId: UUID
    payload: JobPostsCreatePayloadSchema
