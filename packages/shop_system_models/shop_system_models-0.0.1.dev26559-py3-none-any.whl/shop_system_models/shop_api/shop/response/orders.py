from typing import List, Optional
from pydantic import Field

from shop_system_models.shop_api import MetaBaseModel
from shop_system_models.shop_api.shop.request.orders import OrderModel, DeliveryTypeModel
from shop_system_models.shop_api.shop.response.pagination import PaginationResponseModel


class OrderResponseModel(OrderModel):
    """Response model for a single order."""
    id: str


class OrderListResponseModel(MetaBaseModel):
    """Response model for a list of orders."""
    orders: List[OrderResponseModel]
    page_info: PaginationResponseModel


class DeliveryTypeResponseModel(DeliveryTypeModel):
    """Response model for a delivery type."""
    id: str 