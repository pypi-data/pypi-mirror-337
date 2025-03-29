from pydantic import BaseModel
from enum import Enum

class JobAuthOtpPayloadSchema(BaseModel):
    otp: str
