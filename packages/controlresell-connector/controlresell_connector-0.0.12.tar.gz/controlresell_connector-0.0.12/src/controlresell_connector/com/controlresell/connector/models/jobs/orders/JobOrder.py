from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrderStatus import JobOrderStatusSchema

class JobOrderSchema(BaseModel):
    conversationId: str
    transactionId: str
    price: str
    currencyCode: str
    status: JobOrderStatusSchema
    date: str
    transactionUserStatus: str
