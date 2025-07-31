# from Celery_worker.email_worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL
from .email_worker import celery_app, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


'''Задача отправки письма'''
@celery_app.task(name="email.send", bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, event_type, to_email, subject, template_name, data):
    try:
        html_body = render_template(template_name, data)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())

        #logging.info(f"[CELERY EMAIL] Отправлено '{event_type}' письмо на {to_email}")
    except Exception as exc:
        #logging.error(f"[CELERY EMAIL] Ошибка при отправке '{event_type}' на {to_email}: {exc}")
        raise self.retry(exc=exc)

def render_template(template_name: str, data: dict) -> str:
    # Можно использовать Jinja2, как было
    from jinja2 import Template
    if template_name == "registration_confirmation":
        tmpl = Template("Для подтверждения регистрации перейдите по ссылке: <a href='{{ confirmation_link }}'>Подтвердить</a>")
        return tmpl.render(**data)
    # остальные шаблоны...
    return "Шаблон не найден"