from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.depends.admin_check import get_current_admin
from src.utils.db import get_db
from src.admin.schemas import DashboardResponseSchema
from src.admin.service import (
    get_dashboard,
    get_all_orders,
    get_order_by_id,
    update_order_status,
)
from src.admin.schemas import UpdateOrderStatusRequest

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)],
)


# Dashboard

@admin_router.get(
    "/dashboard",
    response_model=DashboardResponseSchema,
)
async def dashboard(
    db: AsyncSession = Depends(get_db),
):
    return await get_dashboard(db)


# Orders

@admin_router.get("/orders")
async def all_orders( db: AsyncSession = Depends(get_db)):
   

    return await get_all_orders(db)


@admin_router.get("/orders/{order_id}")
async def single_order(order_id: int, db: AsyncSession = Depends(get_db)):
    
   

    return await get_order_by_id(order_id, db)


@admin_router.patch("/orders/{order_id}/status")
async def change_order_status(
    order_id: int,
    request: UpdateOrderStatusRequest,
    db: AsyncSession = Depends(get_db),
):
    return await update_order_status(
        order_id=order_id,
        request=request,
        db=db,
    )