from pydantic import BaseModel
from zodable_idschema import Id
from controlresell_connector.com.controlresell.connector.models.accounts.AccountPlatform import AccountPlatform

class CreateAccountPayload(BaseModel):
    platform: AccountPlatform
    ownerId: IdSchema
    credentials: str
