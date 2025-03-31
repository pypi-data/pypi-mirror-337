from pydantic import BaseModel

class JobAuthOtpPayloadSchema(BaseModel):
    otp: str
