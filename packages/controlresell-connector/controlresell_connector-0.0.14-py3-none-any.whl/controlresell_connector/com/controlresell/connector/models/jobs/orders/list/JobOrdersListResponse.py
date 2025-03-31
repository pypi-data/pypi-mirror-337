from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrderSchema

class JobOrdersListResponseSchema(BaseModel):
    orders: list[JobOrderSchema]
