from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from typing import Any

class JobResponseWebhookSchema(BaseModel):
    accountId: UUID
    response: Any
