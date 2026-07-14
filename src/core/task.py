import logging

from celery.exceptions import MaxRetriesExceededError

from src.core.celery import celery_app
from src.core.email import email_utility


logger = logging.getLogger(__name__)


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

        logger.info("Email sent successfully to %s", email_to)

    except MaxRetriesExceededError:
        logger.exception("Maximum retries exceeded for %s", email_to)
        raise

    except Exception:
        logger.exception("Failed to send email to %s", email_to)
        raise