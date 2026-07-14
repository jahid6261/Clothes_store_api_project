from celery import Celery

from src.utils.settings import settings

celery_app = Celery(
    "clothstore",
    broker=settings.CELERY_BROKER_URL,
    backend=None,
    include=[
        "src.core.task",
    ]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    control_queue_exclusive=True,
    event_enable_remote_control=False,
    task_ignore_result=True
)
