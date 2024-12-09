from asgiref.sync import async_to_sync
from celery import Celery
from celery.schedules import crontab

from config import settings
from services.estimates import reset_estimates_number

celery_app = Celery(
    "config",
    broker=settings.CELERY_BROKER_URL,
    backend="rpc://",
)

celery_app.config_from_object(settings)
celery_app.autodiscover_tasks()


@celery_app.task
def reset_estimates_number_task():
    return async_to_sync(reset_estimates_number)()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Importing and adding periodic tasks"""

    sender.add_periodic_task(crontab(hour=0, minute=0), reset_estimates_number_task.s())
