from Service.main import celery_app


# функция для вызова Celery задачи
def send_email_event_celery(event_type, email, subject, template, data):
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