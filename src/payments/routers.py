from fastapi import APIRouter, Depends,Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.payments.schemas import (
    PaymentRequestSchema,
    PaymentResponseSchema,
    PaymentSuccessSchema,
)
from src.payments.service import (create_payment_service,payment_success_service,payment_cancel_service,
                                  payment_fail_service
)


payment_router = APIRouter(prefix="/payment", tags=["Payment"])
    
   



@payment_router.post("/create",response_model=PaymentResponseSchema)
    
    

async def create_payment(
    request: PaymentRequestSchema,
    db: AsyncSession = Depends(get_db),
):

    return await create_payment(
        request=request,
        db=db,
    )


payment_router = APIRouter( prefix="/payment",tags=["Payment"])
   
    
@payment_router.post(  "/create",response_model=PaymentResponseSchema)
async def create_payment(
    request: PaymentRequestSchema,
    db: AsyncSession = Depends(get_db),
):

    return await create_payment_service(
        request=request,
        db=db
    )

@payment_router.post("/success")
async def payment_success(
    tran_id: str = Form(...),
    val_id: str = Form(...),
    amount: str = Form(...),
    status: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    request = PaymentSuccessSchema(
        tran_id=tran_id,
        val_id=val_id,
        amount=amount,
        status=status,
    )

    return await payment_success_service(
        request=request,
        db=db,
    )



@payment_router.post("/cancel")
async def payment_cancel(
    request: PaymentSuccessSchema,
    db: AsyncSession = Depends(get_db),
):

    return await payment_cancel_service(
        request=request,
        db=db
    )

 
@payment_router.post("/fail")
async def payment_fail(
    request: PaymentSuccessSchema,
    db: AsyncSession = Depends(get_db),
):

    return await payment_fail_service(
        request=request,
        db=db
    ) 

    





