from pydantic import BaseModel
from enum import Enum

class JobConversationMessageEntityTypeSchema(str, Enum):
    MESSAGE = 'MESSAGE'
    STATUS_MESSAGE = 'STATUS_MESSAGE'
    ACTION_MESSAGE = 'ACTION_MESSAGE'
