

from pydantic import BaseModel, HttpUrl
from typing import Optional


class PaymentRequestSchema(BaseModel):
    order_id: int



class PaymentResponseSchema(BaseModel):
    status: str
    message: Optional[str] = None
    payment_url: Optional[HttpUrl] = None

class PaymentSuccessSchema(BaseModel):
    tran_id: str
    val_id: str
    amount: str
    status: str    