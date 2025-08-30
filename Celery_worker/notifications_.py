# from Celery_worker.worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL
from .worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, SessionLocal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template
import logging
from sqlalchemy import text
from datetime import datetime

from sqlalchemy.orm import Session
from utils.config import  TIME_NOW

logger = logging.getLogger(__name__)

'''Сохранения лога в основную базу'''
def log_email_to_db(event_type, to_email, subject, template_name, status, error_message=None, retry_count: int = 0):
    session: Session = SessionLocal()
    try:
        now = datetime.strptime(TIME_NOW(), "%Y-%m-%d %H:%M:%S").isoformat() #datetime.utcnow() #TIME_NOW()
        result = session.execute(
            text("""
                UPDATE  EmailLogs SET status=:status,
                    retry_count = retry_count + 1,
                    error_message=:error_message,
                    created_at=:created_at
                WHERE event_type=:event_type AND to_email=:to_email AND subject=:subject AND status='failed'
            """),
            {
                "status": status,
                "error_message": error_message,
                "created_at": now,
                "event_type": event_type,
                "to_email": to_email,
                "subject": subject
            }
        )
        # если ни одной строки не обновилось — создаём новую
        if result.rowcount == 0:
            session.execute(
                text("""
                           INSERT INTO EmailLogs (event_type, to_email, subject, template_name, status, error_message, retry_count, created_at)
                           VALUES (:event_type, :to_email, :subject, :template_name, :status, :error_message, 0, :created_at)
                       """),
                {
                    "event_type": event_type,
                    "to_email": to_email,
                    "subject": subject,
                    "template_name": template_name,
                    "status": status,
                    "error_message": error_message,
                    "created_at": now
                }
            )
        session.commit()
    except Exception as e:
        logging.error(f"[DB] Ошибка записи лога Email: {e}")
        session.rollback()
    finally:
        session.close()

'''Задача отправки письма'''
@celery_app.task(name="email.send", bind=True, max_retries=3, default_retry_delay=60)
def send_email_task______s(self, event_type, to_email, subject, template_name, data):
    logging.info(f"[CELERY EMAIL] Старт задачи отправки email — тип: {event_type}, получатель: {to_email}")

    try:
        html_body = render_template(template_name, data)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        logging.info(f"[CELERY EMAIL] Подключение к SMTP: {SMTP_HOST}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        logging.info(f"[CELERY EMAIL] ✅ Письмо '{event_type}' успешно отправлено на {to_email}")

        log_email_to_db(event_type, to_email, subject, template_name, status="sent")

    except Exception as exc:
        logging.exception(f"[CELERY EMAIL] ❌ Ошибка при отправке '{event_type}' письма на {to_email}: {exc}")
        log_email_to_db(event_type, to_email, subject, template_name, status="failed", error_message=str(exc))
        raise self.retry(exc=exc)

def render_template(template_name: str, data: dict) -> str:
    logging.info(f"[EMAIL TEMPLATE] Запрос шаблона: '{template_name}'")
    logging.info(f"[EMAIL TEMPLATE] Данные для шаблона: {data}")
    # шаблон с письмом для регистрации
    if template_name == "registration_confirmation":
        tmpl = Template("Для подтверждения регистрации перейдите по ссылке: <a href='{{ confirmation_link }}'>Подтвердить</a>")
        return tmpl.render(**data)
    # шаблон с письмом для сброса пароля
    elif template_name == "password_reset":
        tmpl = Template(
            """Для сброса пароля перейдите по ссылке ниже:<br>
        <a href="{{ reset_link }}">{{ reset_link }}</a><br>
        Ссылка действительна {{ expires_hours }} час(а). 
            """)
        return tmpl.render(**data)
    logging.warning(f"[EMAIL TEMPLATE] ❌ Неизвестный шаблон: '{template_name}'")
    return "Шаблон не найден"


def retry_failed_emails(limit: int = 50):
    """
    Берёт N писем со статусом 'failed' и повторно отправляет через Celery.
    """
    session: Session = SessionLocal()
    try:
        # Получаем письма со статусом failed
        failed_emails = session.execute(
            text("""
                SELECT TOP (:limit) id, event_type, to_email, subject, template_name, retry_count
                FROM EmailLogs
                WHERE status = 'failed'
                ORDER BY created_at ASC
            """), {"limit": limit}
        ).fetchall()

        MAX_RETRIES = 3

        for email in failed_emails:
            retry_count = email.retry_count or 0
            if retry_count >= MAX_RETRIES:
                logging.info(f"[RETRY] Превышен лимит повторных попыток для {email.to_email}, пропускаем.")
                continue  # пропускаем письмо

            # Запускаем Celery задачу заново
            send_email_task.apply_async(
                kwargs={
                    "event_type": email.event_type,
                    "to_email": email.to_email,
                    "subject": email.subject,
                    "template_name": email.template_name,
                    "data": email.data if hasattr(email, "data") else {}
                },
                countdown=60 * retry_count
            )
            # Обновляем retry_count
            session.execute(
                text("UPDATE EmailLogs SET retry_count = :retry_count WHERE id = :id"),
                {"retry_count": retry_count + 1, "id": email.id}
            )
        session.commit()
    except Exception as e:
        logging.error(f"[RETRY] Ошибка повторной отправки писем: {e}")
        session.rollback()
    finally:
        session.close()

@celery_app.task(name="email.retry_failed")
def retry_failed_task():
    retry_failed_emails(limit=50)