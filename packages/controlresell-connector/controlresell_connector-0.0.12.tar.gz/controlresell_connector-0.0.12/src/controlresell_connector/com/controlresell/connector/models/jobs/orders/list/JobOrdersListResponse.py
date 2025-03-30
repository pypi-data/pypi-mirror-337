from pydantic import BaseModel
from enum import Enum
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrderSchema

class JobOrdersListResponseSchema(BaseModel):
    orders: JobOrderSchema
