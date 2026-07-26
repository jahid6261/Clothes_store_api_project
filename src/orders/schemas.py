from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Optional


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