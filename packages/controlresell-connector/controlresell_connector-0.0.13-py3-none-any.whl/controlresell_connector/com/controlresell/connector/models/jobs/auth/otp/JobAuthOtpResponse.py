from pydantic import BaseModel
from datetime import datetime

class JobAuthOtpResponseSchema(BaseModel):
    expiresAt: datetime | None
