from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.JobConversationOffer import JobConversationOfferSchema

class JobConversationsOffersCreateResponseSchema(BaseModel):
    accountId: UUID
    offer: JobConversationOfferSchema
