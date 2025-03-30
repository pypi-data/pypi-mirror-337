from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationOppositeUser import JobConversationOppositeUserSchema
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationTransaction import JobConversationTransactionSchema
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessage import JobConversationMessageSchema

class JobConversationSchema(BaseModel):
    conversationId: str
    conversationUrl: str
    subtitle: str
    readByCurrentUser: bool
    readByOppositeUser: bool
    localization: str | None
    translated: bool
    allowReply: bool
    isSuspicious: bool
    isDeletionRestricted: bool
    userHasSupportRole: bool
    safetyEducation: bool
    oppositeUser: JobConversationOppositeUserSchema
    transaction: JobConversationTransactionSchema | None
    messages: JobConversationMessageSchema
