from pydantic import BaseModel
from uuid import UUID
from typing import Any

class JobResponseWebhookSchema(BaseModel):
    accountId: UUID
    response: Any
