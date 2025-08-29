from utils.log import setup_logging

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import os
import logging
from celery.schedules import crontab

#from Service.celery_tasks.notifications import send_email_task
load_dotenv()
import logging
logger = logging.getLogger(__name__)

# Database.py
'''файл с настройкой подключения к основной базе'''
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
# Строка подключения для pymssql
DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    #f"mssql+pyodbc://{DB_HOST}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    #"&trusted_connection=yes"
    "&TrustServerCertificate=yes")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SMTP-параметры
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("EMAIL_FROM", SMTP_USER)


# Настройки Redis
REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")
REDIS_RESULT_BACKEND = os.getenv("REDIS_RESULT_BACKEND")

# Настроим логирование Celery
CELERY_LOG_FILE=os.getenv("CELERY_LOG_FILE")
setup_logging(log_file=CELERY_LOG_FILE)
logging.info(f"[CELERY] Запускаем логирование с файлом: {CELERY_LOG_FILE}")

# Создаём celery app
celery_app = Celery(
    "worker",
    broker=REDIS_BROKER_URL,
    backend=REDIS_RESULT_BACKEND,
    include=["Celery_worker.notifications", "Celery_worker.files"])




# Конфигурация
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    worker_hijack_root_logger=False  # отключаем перехват root logger
)

'''celery_app.conf.beat_schedule = {
    "retry_failed_emails": {
        "task": "email.retry_failed",
        "schedule": crontab(minute="*/1"),  # каждую минуту
    },
}'''
# Проверка подключения к Redis
try:
    redis_client = redis.Redis.from_url(REDIS_BROKER_URL)
    redis_client.ping()
    #print("✅ Подключение к Redis успешно установлено.")
    logging.info("[CELERY]✅ Подключение к Redis успешно установлено.")
except redis.exceptions.ConnectionError as e:
    print(f"[CELERY]❌ Ошибка подключения к Redis: {e}")
    raise SystemExit("Не удалось подключиться к Redis — проверь docker-compose, порты и настройки.")

# celery_app.autodiscover_tasks(['Service.celery_tasks'])
# celery_app.conf.task_routes = {
#     "Service.celery_tasks.notifications.send_email_task": {"queue": "emails"},
# }