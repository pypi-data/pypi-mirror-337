from pydantic import BaseModel
from enum import Enum

class JobOrderSchema(BaseModel):
    brand: str
    catalogId: int
    colorIds: int
    description: str
    measurementLength: float | None
    measurementWidth: float | None
    packageSizeId: int
    photoUrls: str
    price: float
    sizeId: int | None
    statusId: int
    title: str
    isDraft: bool
    material: int
    manufacturerLabelling: str | None
