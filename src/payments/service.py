import requests
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload
from src.orders.models import Order,Cart
from src.products.models import ProductVariant
from src.payments.sslcommerz import SSLCommerz
from src.payments.schemas import PaymentRequestSchema,PaymentSuccessSchema
from src.core.task import send_email_service

async def create_payment_service(
    request: PaymentRequestSchema,
    db: AsyncSession,
):

    result = await db.execute(
        select(Order)
        .where(Order.id == request.order_id)
    )

    order = result.scalar_one_or_none()


    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )


    if order.paid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already paid."
        )


    sslcommerz = SSLCommerz()
    payload = {
    "store_id": sslcommerz.store_id,
    "store_passwd": sslcommerz.store_password,

    "total_amount": str(order.total_price),
    "currency": "BDT",
    "tran_id": f"ORDER_{order.id}",

    "success_url": sslcommerz.success_url,
    "fail_url": sslcommerz.fail_url,
    "cancel_url": sslcommerz.cancel_url,

    "cus_name": f"{order.first_name} {order.last_name}",
    "cus_email": order.email,
    "cus_phone": order.phone,
    "cus_add1": order.address,
    "cus_city": order.city,
    "cus_postcode": order.postal_code,
    "cus_country": "Bangladesh",

    
    "ship_name": f"{order.first_name} {order.last_name}",
    "ship_add1": order.address,
    "ship_city": order.city,
    "ship_postcode": order.postal_code,
    "ship_country": "Bangladesh",

    "shipping_method": "NO",

    "product_name": "Clothing Product",
    "product_category": "Clothing",
    "product_profile": "general",
}



    response = sslcommerz.create_payment(payload)
    print(response)


    if response.get("status") != "SUCCESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment session creation failed."
        )


    return {
        "status": "success",
        "message": "Payment session created",
        "payment_url": response.get("GatewayPageURL"),
    }




async def payment_success_service(
    request: PaymentSuccessSchema,
    db: AsyncSession,
):

    try:
        order_id = int(request.tran_id.split("_")[1])

        result = await db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_items))
        )

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        if order.paid:
            raise HTTPException(
                status_code=400,
                detail="Payment already completed."
            )

        sslcommerz = SSLCommerz()

        response = requests.get(
            sslcommerz.validation_url,
            params={
                "val_id": request.val_id,
                "store_id": sslcommerz.store_id,
                "store_passwd": sslcommerz.store_password,
            },
            timeout=30
        )

        data = response.json()

        if data.get("status") != "VALID":
            raise HTTPException(
                status_code=400,
                detail="Payment validation failed."
            )

        order.paid = True
        order.transaction_id = request.val_id

        for item in order.order_items:
            if item.variant_id:
                result = await db.execute(
                    select(ProductVariant)
                    .where(ProductVariant.id == item.variant_id)
                )

                variant = result.scalar_one_or_none()

                if variant:
                    if variant.stock < item.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail="Insufficient stock."
                        )

                    variant.stock -= item.quantity

        result = await db.execute(
            select(Cart)
            .where(Cart.user_id == order.user_id)
            .options(selectinload(Cart.cart_items))
        )

        cart = result.scalar_one_or_none()

        if cart:
            for item in cart.cart_items:
                await db.delete(item)

        await db.commit()
        await db.refresh(order)

        send_email_service.delay(
            email_to=order.email,
            email_subject=f"Payment Successful - Order #{order.id}",
            email_body=f"""
Hello {order.first_name},

Your payment has been completed successfully.

Order ID: {order.id}
Amount: {order.total_price} BDT
Transaction ID: {order.transaction_id}

Thank you for shopping with us.
"""
        )

        return {
            "status": "success",
            "message": "Payment completed successfully",
            "order_id": order.id
        }

    except HTTPException:
        await db.rollback()
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def payment_cancel_service(
    request: PaymentSuccessSchema,
    db: AsyncSession,
):

    try:
        order_id = int(request.tran_id.split("_")[1])

        result = await db.execute(
            select(Order)
            .where(Order.id == order_id)
        )

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        return {
            "status": "cancelled",
            "message": "Payment cancelled by user.",
            "order_id": order.id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )   



async def payment_fail_service(
    request: PaymentSuccessSchema,
    db: AsyncSession,
):

    try:
        order_id = int(request.tran_id.split("_")[1])

        result = await db.execute(
            select(Order)
            .where(Order.id == order_id)
        )

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        return {
            "status": "failed",
            "message": "Payment failed.",
            "order_id": order.id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )    