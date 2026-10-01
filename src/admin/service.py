from fastapi import HTTPException, status
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.orders.models import Order,OrderStatus,OrderItem
from src.products.models import Category,Product
from src.users.models import UserModel
from src.admin.schemas import UpdateOrderStatusRequest

async def get_all_orders(db: AsyncSession):
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.user),
            selectinload(Order.order_items),
        )
        .order_by(Order.created_at.desc())
    )

    orders = result.scalars().all()

    return [
        {
            "id": order.id,
            "first_name": order.user.first_name,
            "last_name": order.user.last_name,
            "email": order.user.email,
            "phone": order.phone,

            "address": order.address,
            "city": order.city,
            "postal_code": order.postal_code,

            "total_price": order.total_price,
            "paid": order.paid,
            "transaction_id": order.transaction_id,
            "status": order.status,
            "created_at": order.created_at,

            "order_items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "price": item.price,
                    "quantity": item.quantity,
                    "total_price": item.total_price,
                }
                for item in order.order_items
            ],
        }
        for order in orders
    ]


async def get_order_by_id(order_id: int, db: AsyncSession):
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.user),
            selectinload(Order.order_items),
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return {
        "id": order.id,
        "first_name": order.user.first_name,
        "last_name": order.user.last_name,
        "email": order.user.email,
        "phone": order.phone,

        "address": order.address,
        "city": order.city,
        "postal_code": order.postal_code,

        "total_price": order.total_price,
        "paid": order.paid,
        "transaction_id": order.transaction_id,
        "status": order.status,
        "created_at": order.created_at,

        "order_items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "variant_id": item.variant_id,
                "price": item.price,
                "quantity": item.quantity,
                "total_price": item.total_price,
            }
            for item in order.order_items
        ],
    }


async def update_order_status(
    order_id: int,
    request: UpdateOrderStatusRequest,
    db: AsyncSession,
):
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(
            selectinload(Order.user),
            selectinload(Order.order_items),
        )
    )

    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    order.status = request.status

    await db.commit()
    await db.refresh(order)

    return {
        "success": True,
        "message": "Order status updated successfully",
        "data": order,
    }



async def get_dashboard(db: AsyncSession):
    total_users = await db.scalar(
        select(func.count(UserModel.id))
    ) or 0

    total_categories = await db.scalar(
        select(func.count(Category.id))
    ) or 0

    total_products = await db.scalar(
        select(func.count(Product.id))
    ) or 0

    total_orders = await db.scalar(
        select(func.count(Order.id))
    ) or 0

    pending_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.status == OrderStatus.PENDING)
    ) or 0

    processing_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.status == OrderStatus.PROCESSING)
    ) or 0

    shipped_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.status == OrderStatus.SHIPPED)
    ) or 0

    delivered_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.status == OrderStatus.DELIVERED)
    ) or 0

    cancelled_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.status == OrderStatus.CANCELLED)
    ) or 0

    paid_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.paid == True)
    ) or 0

    unpaid_orders = await db.scalar(
        select(func.count(Order.id))
        .where(Order.paid == False)
    ) or 0

    total_sales = await db.scalar(
        select(func.coalesce(func.sum(OrderItem.total_price), 0))
        .join(Order, Order.id == OrderItem.order_id)
        .where(Order.paid == True)
    ) or 0

    return {
        "total_users": total_users,
        "total_categories": total_categories,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "paid_orders": paid_orders,
        "unpaid_orders": unpaid_orders,
        "total_sales": float(total_sales),
    }




