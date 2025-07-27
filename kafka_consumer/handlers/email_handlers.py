import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from jinja2 import Template  # для шаблонов
import os
from dotenv import load_dotenv
from smtplib import SMTPNotSupportedError
from email.header import Header
logger = logging.getLogger(__name__)

load_dotenv()
# 🔐 SMTP-параметры (вынеси в .env и загрузи через os.getenv)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("EMAIL_FROM", SMTP_USER)

# для продакшн
def handle_email_event(message: dict):
    event_type = message.get("event_type")
    to_email = message.get("email")
    subject = message.get("subject")
    template_name = message.get("template")
    data = message.get("data", {})

    try:
        # Заглушка: рендер шаблона
        html_body = render_template(template_name, data)

        # Формируем письмо
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Bcc"] = "Beginin-Oleg@yandex.ru"
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        recipients = [to_email, "Beginin-Oleg@yandex.ru"]
        # Отправка
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, recipients, msg.as_string())

        logger.info(f"[EMAIL] Отправлено '{event_type}' письмо на {to_email}")
    except Exception as e:
        logger.exception(f"[EMAIL] Ошибка отправки email ({event_type}) на {to_email}: {e}")

# для теста через Mailhog
'''def handle_email_event(message: dict):
    event_type    = message.get("event_type")
    to_email      = message.get("email")
    subject       = message.get("subject")
    template_name = message.get("template")
    data          = message.get("data", {})

    try:
        # Генерируем HTML-тело письма
        html_body = render_template(template_name, data)

        # Формируем MIME-письмо с кодировкой UTF-8
        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"]    = FROM_EMAIL
        msg["To"]      = to_email

        html_part = MIMEText(html_body, "html", "utf-8")
        msg.attach(html_part)

        # Отправляем через SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            # Задаем кодировку команд SMTP
            server.command_encoding = 'utf-8'
            # Если нужны учётные данные — логинимся
            if SMTP_USER and SMTP_PASS:
                server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_bytes())

        logger.info(f"[EMAIL] ({event_type}) письмо отправлено: {to_email}")

    except Exception as e:
        logger.exception(f"[EMAIL] Ошибка при отправке ({event_type}) на {to_email}: {e}")'''




def render_template(template_name: str, data: dict) -> str:
    # Заглушка шаблона. Потом заменишь на чтение из .html файлов
    if template_name == "registration_confirmation":
        tmpl = Template("Для подтверждения регистрации перейдите по ссылке: <a href='{{ confirmation_link }}'>Подтвердить</a>")
        return tmpl.render(**data)
    elif template_name == "reset_password":
        tmpl = Template("Чтобы сбросить пароль, перейдите по ссылке: <a href='{{ reset_link }}'>Сбросить</a>")
        return tmpl.render(**data)
    else:
        return "Шаблон не найден"