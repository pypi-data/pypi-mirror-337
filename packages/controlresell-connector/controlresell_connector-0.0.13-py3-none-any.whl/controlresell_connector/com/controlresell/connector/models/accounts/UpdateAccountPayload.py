from pydantic import BaseModel

class UpdateAccountPayloadSchema(BaseModel):
    credentials: str | None
    data: str | None
