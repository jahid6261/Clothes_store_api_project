from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.orders.schemas import (
    CartItemCreateSchema,
    CartItemResponseSchema
)

from src.orders.service import add_to_cart

from src.depends.auth_depends import get_current_user


orders_router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@orders_router.post(
    "/items",
    response_model=CartItemResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_cart_item(
    request: CartItemCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):

    cart_item = await add_to_cart(
        user_id=current_user.id,
        request=request,
        db=db
    )

    return cart_item