from Service.celery_tasks.celery_app import celery_app
from Service.Schemas.auth import EmailRequest
from Service.dependencies import get_db
from Service.Models import EmailLog

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from sqlalchemy import text
import logging
logger = logging.getLogger(__name__)

celery_router = APIRouter(prefix="/api/auth", tags=["auth"]) # страница для пользователей


'''создаем запись в таблице и id данной записи отправляем в очередь Celery'''
@celery_router.post("/send-email") # только если использую через http запрос
def send_email_event_celery(request: EmailRequest, event_type: str, db: Session = Depends(get_db)):
    logging.info(f"[EMAIL_SENDER]: запуск функции send_email_event_celery")
    # Создаём объект
    new_email=EmailLog(
        event_type=event_type,  # <- сохраняем тип события
        to_email=request.to_email,
        subject=request.subject,
        body=request.body,
        status="pending",
        retry_count=0
    )
    db.add(new_email)  # добавляем в сессию
    db.commit()
    db.refresh(new_email)  # получаем id

    # Отправляем задачу в Celery
    celery_app.send_task(
        name="email.send",
        kwargs={"email_id": new_email.id}
    )

    return {"message": "Email queued", "email_id": new_email.id}



def send_files(event_type, email, subject, template, data):
    logging.info(f"[EMAIL_SENDER]: запуск функции send_files")
    celery_app.send_task(
        name="save_subtask_files",
        kwargs={
            "event_type": event_type,
            "to_email": email,
            "subject": subject,
            "template_name": template,
            "data": data
        }
    )

# функция для вызова Celery задачи
def send_email(event_type, email, subject, template, data):
    logging.info(f"[EMAIL_SENDER]: запуск функции send_email")
    celery_app.send_task(
        name="email.send",  # Имя должно совпадать с тем, что указано в @task(name=...)
        kwargs={
            "event_type": event_type,
            "to_email": email,
            "subject": subject,
            "template_name": template,
            "data": data
        }
    )