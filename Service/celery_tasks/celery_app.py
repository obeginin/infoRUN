from celery import Celery
import os

REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")
# подключить Celery клиент
celery_app = Celery(
    'email_sender',
    broker=REDIS_BROKER_URL,
    include=["Celery_worker.notifications"]
)
