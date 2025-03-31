from pydantic import BaseModel

class JobConversationOffer(BaseModel):
    id: str
    price: str
    currency: str
    userMsgThreadId: str
    transactionId: str
