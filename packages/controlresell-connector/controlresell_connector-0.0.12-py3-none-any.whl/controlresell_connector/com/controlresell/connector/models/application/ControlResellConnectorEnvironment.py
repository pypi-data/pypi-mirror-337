from pydantic import BaseModel
from enum import Enum

class ControlResellConnectorEnvironmentSchema(str, Enum):
    PRODUCTION = 'PRODUCTION'
    STAGING = 'STAGING'
