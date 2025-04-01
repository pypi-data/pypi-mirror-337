from enum import Enum

class JobConversationMessageType(str, Enum):
    MESSAGE = 'MESSAGE'
    STATUS_MESSAGE = 'STATUS_MESSAGE'
    ACTION_MESSAGE = 'ACTION_MESSAGE'
