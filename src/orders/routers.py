from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.depends.auth_depends import get_current_user
from src.orders.schemas import (
    CartItemCreateSchema,
    CartItemResponseSchema,
    CartResponseSchema,
    CartItemUpdateSchema,
    CheckoutResponseSchema,
    CreateOrderSchema,
    OrderResponseSchema,
)
from src.orders.service import (
    add_to_cart,
    get_cart_service,
    update_cart_item,
    delete_cart_item,
    clear_user_cart,
    checkout,
    create_order_service,
    get_my_orders,
    get_order_by_id,
    cancel_order_service,
)
from src.utils.db import get_db


cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.post("/items", response_model=CartItemResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    request: CartItemCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await add_to_cart(user_id=current_user.id, request=request, db=db)


@cart_router.get("", response_model=CartResponseSchema)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_cart_service(user_id=current_user.id, db=db)


@cart_router.patch("/items/{item_id}", response_model=CartItemResponseSchema)
async def update_cart(
    item_id: int,
    request: CartItemUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await update_cart_item(
        user_id=current_user.id,
        item_id=item_id,
        request=request,
        db=db,
    )


@cart_router.delete("/items/{item_id}")
async def remove_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await delete_cart_item(user_id=current_user.id, item_id=item_id, db=db)


@cart_router.delete("/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await clear_user_cart(user_id=current_user.id, db=db)


@cart_router.post("/checkout", response_model=CheckoutResponseSchema)
async def checkout_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await checkout(current_user.id, db)


# Order Router

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/create", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await create_order_service(request=request, user_id=current_user.id, db=db)


@order_router.get("", response_model=list[OrderResponseSchema])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_my_orders(user_id=current_user.id, db=db)


@order_router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_order_by_id(order_id=order_id, user_id=current_user.id, db=db)


@order_router.patch("/{order_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await cancel_order_service(order_id=order_id, user_id=current_user.id, db=db)