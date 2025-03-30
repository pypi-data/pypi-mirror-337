from pydantic import BaseModel
from enum import Enum

class JobPostOptionalsSchema(BaseModel):
    brand: str | None
    catalogId: int | None
    colorIds: int
    description: str | None
    measurementLength: float | None
    measurementWidth: float | None
    packageSizeId: int | None
    photoUrls: str
    price: float | None
    sizeId: int | None
    statusId: int | None
    title: str | None
    isDraft: bool | None
    material: int
    manufacturerLabelling: str | None
