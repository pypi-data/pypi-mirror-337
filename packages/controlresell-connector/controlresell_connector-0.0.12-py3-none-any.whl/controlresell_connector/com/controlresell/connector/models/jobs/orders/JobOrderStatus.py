from pydantic import BaseModel
from enum import Enum

class JobOrderStatusSchema(str, Enum):
    PAYMENT_VALIDATED = 'PAYMENT_VALIDATED'
    SHIPPING_LABEL_SENT_TO_SELLER = 'SHIPPING_LABEL_SENT_TO_SELLER'
