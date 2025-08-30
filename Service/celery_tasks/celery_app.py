from celery import Celery
import os
import logging
logger = logging.getLogger(__name__)

REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")
# подключить Celery клиент к брокеру сообщений (туда отправляем ставим задачи в очередь)
celery_app = Celery(
    'celery',
    broker=REDIS_BROKER_URL,
    include=["Celery_worker.notifications", "Celery_worker.files"]
)
