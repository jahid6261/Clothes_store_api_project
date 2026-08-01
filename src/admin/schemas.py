from pydantic import BaseModel
from src.orders.models import OrderStatus

class UpdateOrderStatusRequest(BaseModel):
    status:OrderStatus 


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