from pydantic import BaseModel
from enum import Enum
from zodable_idschema import IdSchema
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatformSchema

class AccountSchema(BaseModel):
    id: UUID
    platform: AccountPlatformSchema
    ownerId: IdSchema
    credentials: str | None
    data: str | None
