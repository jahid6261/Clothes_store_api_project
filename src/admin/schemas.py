from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.orders.models import OrderStatus


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus


class DashboardResponseSchema(BaseModel):
    total_users: int
    total_categories: int
    total_products: int
    total_orders: int
    pending_orders: int
    processing_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int
    paid_orders: int
    unpaid_orders: int
    total_sales: float


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int] = None
    price: float
    quantity: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class AdminOrderResponse(BaseModel):
    id: int

    first_name: str
    last_name: str
    email: str
    phone: str

    address: str
    city: str
    postal_code: str

    total_price: float
    paid: bool
    transaction_id: Optional[str] = None
    status: str
    created_at: datetime

    order_items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)