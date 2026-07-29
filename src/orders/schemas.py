from pydantic import BaseModel, ConfigDict, Field,EmailStr
from decimal import Decimal
from typing import Optional
from datetime import datetime
from src.orders.models import OrderStatus
# -----------------------------
# Product Response in Cart
# -----------------------------

class CartProductResponseSchema(BaseModel):
    id: int
    name: str
    price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Image Response in Variant
# -----------------------------

class CartImageResponseSchema(BaseModel):
    id: int
    image_url: str
    public_id: str

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Variant Response in Cart
# -----------------------------

class CartVariantResponseSchema(BaseModel):
    id: int
    size: str
    color: str
    sku: str

    images: list[CartImageResponseSchema] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Add Cart Item
# -----------------------------

class CartItemCreateSchema(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(
        default=1,
        gt=0
    )


# -----------------------------
# Update Quantity
# -----------------------------

class CartItemUpdateSchema(BaseModel):
    quantity: int = Field(
        ...,
        gt=0
    )


# -----------------------------
# Cart Item Response
# -----------------------------

class CartItemResponseSchema(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int]
    quantity: int

    product: CartProductResponseSchema
    variant: Optional[CartVariantResponseSchema] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------
# Cart Response
# -----------------------------

class CartResponseSchema(BaseModel):
    id: int
    user_id: int

    cart_items: list[CartItemResponseSchema] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )


class CheckoutItemResponseSchema(BaseModel):
    product_id: int
    product_name: str
    variant_id: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
    price: Decimal
    quantity: int
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class CheckoutResponseSchema(BaseModel):
    items: list[CheckoutItemResponseSchema]
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)    



class CreateOrderSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str
    city: str
    postal_code: str
    note: Optional[str] = None

class OrderItemResponseSchema(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    price: Decimal
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponseSchema(BaseModel):
    id: int
    user_id: int

    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    address: str
    city: str
    postal_code: str
    note: Optional[str]

    total_price: Decimal
    paid: bool
    transaction_id: Optional[str]
    status: OrderStatus

    created_at: datetime

    order_items: list[OrderItemResponseSchema]

    model_config = ConfigDict(from_attributes=True)

