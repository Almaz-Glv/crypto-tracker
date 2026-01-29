from celery import Celery
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

# Используем PostgreSQL как брокер
broker_url = "redis://localhost:6379/0"
backend_url = broker_url

logger.info(f"Using PostgreSQL as Celery broker: {broker_url}")

celery_app = Celery(
    "crypto_tracker",
    broker=broker_url,
    backend=backend_url,
    include=["src.application.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    
    # Расписание
    beat_schedule={
        'fetch-prices-every-minute': {
            'task': 'src.application.tasks.fetch_and_store_prices_task',
            'schedule': 60.0,
        },
    },
)
