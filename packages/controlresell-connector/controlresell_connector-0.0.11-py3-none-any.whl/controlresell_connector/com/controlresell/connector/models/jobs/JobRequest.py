from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.accounts.Account import AccountSchema
from typing import Any

class JobRequestSchema(BaseModel):
    account: AccountSchema
    payload: Any
