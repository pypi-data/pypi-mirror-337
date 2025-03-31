from pydantic import BaseModel
from zodable_idschema import Id

class JobPostsCreateResponse(BaseModel):
    platformId: str
    platformUrl: str
    platformPrice: float
    itemId: IdSchema
