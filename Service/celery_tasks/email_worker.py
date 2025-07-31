from celery import Celery
from dotenv import load_dotenv
import redis
import os
#from Service.celery_tasks.notifications import send_email_task
load_dotenv()
# SMTP-параметры
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("EMAIL_FROM", SMTP_USER)


# Настройки Redis
REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")
REDIS_RESULT_BACKEND = os.getenv("REDIS_RESULT_BACKEND")

# Создаём celery app
celery_app = Celery("email_sender", broker=REDIS_BROKER_URL, backend=REDIS_RESULT_BACKEND, include=["Service.celery_tasks.notifications"])

# Конфигурация
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)
# Проверка подключения к Redis
try:
    redis_client = redis.Redis.from_url(REDIS_BROKER_URL)
    redis_client.ping()
    print("✅ Подключение к Redis успешно установлено.")
    #logging.info("✅ Подключение к Redis успешно установлено.")
except redis.exceptions.ConnectionError as e:
    print(f"❌ Ошибка подключения к Redis: {e}")
    raise SystemExit("Не удалось подключиться к Redis — проверь docker-compose, порты и настройки.")

# celery_app.autodiscover_tasks(['Service.celery_tasks'])
# celery_app.conf.task_routes = {
#     "Service.celery_tasks.notifications.send_email_task": {"queue": "emails"},
# }