from pydantic import BaseModel
from enum import Enum
from zodable_idschema import IdSchema

class JobPostsCreateResponseSchema(BaseModel):
    platformId: str
    platformUrl: str
    platformPrice: float
    itemId: IdSchema
