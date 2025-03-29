from pydantic import BaseModel
from enum import Enum

class JobAuthDataResponseSchema(BaseModel):
    id: str
