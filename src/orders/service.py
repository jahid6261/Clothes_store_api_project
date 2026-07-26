from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.products.models import Product, ProductVariant
from src.orders.models import Cart, CartItem
from src.orders.schemas import CartItemCreateSchema


async def add_to_cart(
    user_id: int,
    request: CartItemCreateSchema,
    db: AsyncSession
):

    # Step 1: Get user's cart
    cart = await db.scalar(
        select(Cart).where(
            Cart.user_id == user_id
        )
    )


    # Create cart if user has no cart
    if not cart:

        cart = Cart(
            user_id=user_id
        )

        db.add(cart)
        await db.flush()


    # Step 2: Check product exists
    product = await db.scalar(
        select(Product).where(
            Product.id == request.product_id
        )
    )


    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


    # Step 3: Validate variant
    variant = None

    if request.variant_id:

        variant = await db.scalar(
            select(ProductVariant).where(
                ProductVariant.id == request.variant_id,
                ProductVariant.product_id == request.product_id
            )
        )


        if not variant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Variant not found"
            )


        if variant.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )


    # Step 4: Check existing cart item
    cart_item = await db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == request.product_id,
            CartItem.variant_id == request.variant_id
        )
    )


    # Step 5: Update existing item quantity
    if cart_item:

        new_quantity = (
            cart_item.quantity + request.quantity
        )


        if variant and variant.stock < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )


        cart_item.quantity = new_quantity


    # Step 6: Create new cart item
    else:

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=request.product_id,
            variant_id=request.variant_id,
            quantity=request.quantity
        )

        db.add(cart_item)


    await db.commit()
    await db.refresh(cart_item)

    return cart_item