import logging

from src.core.celery import celery_app
from src.core.email import email_utility
from src.utils.settings import settings


logger = logging.getLogger(__name__)


# =========================================================
# Common Celery Email Task
# =========================================================

@celery_app.task(
    bind=True,
    name="send_email_service",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
)
def send_email_service(
    self,
    email_to: str,
    email_subject: str,
    email_body: str,
) -> None:

    try:
        email_utility(
            email_to=email_to,
            email_subject=email_subject,
            email_body=email_body,
        )

        logger.info(
            "Email sent successfully to %s",
            email_to,
        )

    except Exception:
        logger.exception(
            "Failed to send email to %s",
            email_to,
        )
        raise


# =========================================================
# Account Activation Email
# =========================================================

def send_activation_email(
    to_email: str,
    first_name: str,
    activation_token: str,
) -> None:

    activation_url = (
        f"{settings.BASE_URL}/api/v1/users/activate/{activation_token}"
    )

    email_body = f"""
Hello {first_name},

Welcome to Cloth Store Team.

Your account has been created successfully.

Please click the link below to activate your account:

{activation_url}

After activating your account, you will be able to login.

If you did not create this account, please ignore this email.

Best regards,
Cloth Store Team
"""

    send_email_service.delay(
        email_to=to_email,
        email_subject="Cloth Store - Activate Your Account",
        email_body=email_body,
    )


# =========================================================
# Password Reset OTP Email
# =========================================================

def send_password_reset_otp_email(
    to_email: str,
    first_name: str,
    otp: str,
) -> None:

    email_body = f"""
Hello {first_name},

We received a request to reset the password for your Cloth Store account.

Your password reset OTP is:

{otp}

This OTP will expire in 5 minutes.

If you did not request a password reset, you can safely ignore this email.

Best regards,
Cloth Store Team
"""

    send_email_service.delay(
        email_to=to_email,
        email_subject="Cloth Store - Password Reset OTP",
        email_body=email_body,
    )

def send_payment_success_email(
    to_email: str,
    first_name: str,
    order_id: int,
    amount,
    transaction_id: str,
) -> None:

    email_body = f"""
Hello {first_name},

Your payment has been completed successfully.

Order ID: {order_id}
Amount: {amount} BDT
Transaction ID: {transaction_id}

Thank you for shopping with us.

Best regards,
Cloth Store Team
"""

    send_email_service.delay(
        email_to=to_email,
        email_subject=f"Cloth Store - Payment Successful - Order #{order_id}",
        email_body=email_body,
    )
