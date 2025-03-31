from enum import Enum

class JobConversationMessageEntityType(str, Enum):
    MESSAGE = 'MESSAGE'
    STATUS_MESSAGE = 'STATUS_MESSAGE'
    ACTION_MESSAGE = 'ACTION_MESSAGE'
