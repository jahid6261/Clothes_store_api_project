from sqlalchemy import Column, Integer, DateTime, ForeignKey,Numeric,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.utils.db import DBModel


class Cart(DBModel):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("UserModel", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(DBModel):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            "variant_id",
            name="uq_cart_product_variant"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    variant_id = Column(
    Integer,
    ForeignKey(
        "product_variants.id",
        ondelete="SET NULL"
    ),
    nullable=True
)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    variant = relationship(
    "ProductVariant",
    back_populates="cart_items"
)



    