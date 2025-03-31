from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.offers.JobConversationOffer import JobConversationOffer

class JobConversationsOffersCreateResponse(BaseModel):
    accountId: UUID
    offer: JobConversationOffer
