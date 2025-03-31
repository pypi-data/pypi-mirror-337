from pydantic import BaseModel

class JobPostOptionalsSchema(BaseModel):
    brand: str | None
    catalogId: int | None
    colorIds: list[int] | None
    description: str | None
    measurementLength: float | None
    measurementWidth: float | None
    packageSizeId: int | None
    photoUrls: list[str] | None
    price: float | None
    sizeId: int | None
    statusId: int | None
    title: str | None
    isDraft: bool | None
    material: list[int] | None
    manufacturerLabelling: str | None
