from pydantic import BaseModel

class JobConversationOfferSchema(BaseModel):
    id: str
    price: str
    currency: str
    userMsgThreadId: str
    transactionId: str
