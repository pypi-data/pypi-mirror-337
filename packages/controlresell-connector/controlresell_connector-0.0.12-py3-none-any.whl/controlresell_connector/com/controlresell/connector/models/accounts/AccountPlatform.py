from pydantic import BaseModel
from enum import Enum

class AccountPlatformSchema(str, Enum):
    VINTED = 'VINTED'
    SHOPIFY = 'SHOPIFY'
