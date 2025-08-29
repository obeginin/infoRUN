from Celery_worker.email_worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, SessionLocal

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

MAX_RETRIES = 3

@celery_app.task(bind=True, name="email.send", max_retries=3)
def send_email_task(self, email_id: int):
    db = SessionLocal()
    try:
        email_log = db.execute(
            text("SELECT * FROM EmailLogs WHERE id = :email_id"),
            {"email_id": email_id}
        ).mappings().first()

        if not email_log:
            return

        if email_log.status == "sent" or email_log["retry_count"] >= MAX_RETRIES:
            return

        try:
            # --- SMTP отправка ---
            msg = MIMEMultipart("alternative")
            msg["Subject"] = email_log["subject"]
            msg["From"] = FROM_EMAIL
            msg["To"] = email_log["to_email"]
            msg.attach(MIMEText(email_log["body"], "plain", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(FROM_EMAIL, [email_log["to_email"]], msg.as_string())

            # успешная отправка
            db.execute(
                text("UPDATE EmailLogs SET status='sent', sent_at=:sent_at WHERE id=:id"),
                {"sent_at": datetime.utcnow(), "id": email_log.id}
            )
            db.commit()

        except Exception as e:
            # увеличиваем retry_count
            db.execute(text(
                "UPDATE EmailLogs SET status='failed', retry_count=retry_count+1 WHERE id=:id"),
                {"id": email_id}
            )
            db.commit()
            if email_log["retry_count"] + 1 < MAX_RETRIES:
                raise self.retry(exc=e, countdown=60)

        db.commit()
    finally:
        db.close()

'''def render_template(template_name: str, data: dict) -> str:
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
    return "Шаблон не найден"'''

