from pydantic import BaseModel
from enum import Enum

class JobConversationOfferSchema(BaseModel):
    id: str
    price: str
    currency: str
    userMsgThreadId: str
    transactionId: str
