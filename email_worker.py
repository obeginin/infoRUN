from config_celery import celery_app
from Service.celery_tasks.notifications import send_email_task  # обязательно импортируем задачу

# Ничего вызывать не нужно, главное — чтобы Celery видел все задачи
# Celery сам подхватит задачи из импортированных модулей