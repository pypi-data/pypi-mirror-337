from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class JobAuthOtpResponseSchema(BaseModel):
    expiresAt: datetime | None
