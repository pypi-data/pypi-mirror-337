from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.accounts.Account import AccountSchema
from typing import Any

class JobRequestSchema(BaseModel):
    account: AccountSchema
    payload: Any
