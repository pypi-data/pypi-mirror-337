from pydantic import BaseModel

class JobPostSchema(BaseModel):
    brand: str
    catalogId: int
    colorIds: list[int] | None
    description: str
    measurementLength: float | None
    measurementWidth: float | None
    packageSizeId: int
    photoUrls: list[str]
    price: float
    sizeId: int | None
    statusId: int
    title: str
    isDraft: bool
    material: list[int] | None
    manufacturerLabelling: str | None
