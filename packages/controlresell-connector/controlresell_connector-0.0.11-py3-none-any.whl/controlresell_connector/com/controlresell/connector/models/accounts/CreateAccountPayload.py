from pydantic import BaseModel
from enum import Enum
from zodable_idschema import IdSchema
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatformSchema

class CreateAccountPayloadSchema(BaseModel):
    platform: AccountPlatformSchema
    ownerId: IdSchema
    credentials: str
