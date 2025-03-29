from pydantic import BaseModel
from enum import Enum

class JobConversationTransactionSchema(BaseModel):
    id: int
    status: int
    offlineVerification: bool | None
    offerId: int | None
    buyerId: int | None
    sellerId: int | None
    isCompleted: bool | None
    shippingOrderId: int | None
    availableActions: str
    currentUserSide: str | None
    isBundle: bool | None
    isReserved: bool | None
    isPackageSizeSelected: bool | None
    isBusinessSeller: bool | None
    itemCount: int | None
    itemId: int | None
    itemIds: int
    itemTitle: str | None
    itemUrl: str | None
    itemIsClosed: bool | None
    offerPriceAmount: str | None
    offerPriceCurrency: str | None
    serviceFeeAmount: str | None
    serviceFeeCurrency: str | None
    shipmentPriceAmount: str | None
    shipmentPriceCurrency: str | None
    totalWithoutShipmentAmount: str | None
    totalWithoutShipmentCurrency: str | None
    totalAmountWithoutTax: str | None
    sellerItemCount: int | None
    sellerCity: str | None
    shipmentId: int | None
    shipmentStatus: int | None
    packageSizeCode: str | None
