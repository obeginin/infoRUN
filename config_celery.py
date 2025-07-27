
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
# SMTP-параметры
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("EMAIL_FROM", SMTP_USER)


celery_app = Celery(
    "email_sender",
    broker="redis://localhost:6379/0",  # Redis как брокер
    backend="redis://localhost:6379/1"  # Redis как хранилище результатов
)

celery_app.conf.task_routes = {
    "worker.tasks.send_email": {"queue": "emails"},
}