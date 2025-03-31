from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrderStatus import JobOrderStatus

class JobOrder(BaseModel):
    conversationId: str
    transactionId: str
    price: str
    currencyCode: str
    status: JobOrderStatus
    date: str
    transactionUserStatus: str
