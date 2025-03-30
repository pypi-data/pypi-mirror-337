from pydantic import BaseModel
from enum import Enum

class UpdateAccountPayloadSchema(BaseModel):
    credentials: str | None
    data: str | None
