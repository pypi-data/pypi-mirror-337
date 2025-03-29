from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.auth.otp.JobAuthOtpPayload import JobAuthOtpPayloadSchema

class JobAuthOtpWithAccountPayloadSchema(BaseModel):
    accountId: UUID
    payload: JobAuthOtpPayloadSchema
