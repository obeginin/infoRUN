from kafka import KafkaProducer
from dotenv import load_dotenv
from config_app import TIME_NOW
from kafka.errors import KafkaError
import json
from datetime import datetime
import pytz
import logging
import os
logger = logging.getLogger(__name__)

load_dotenv()
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
_producer = None

# События (action_type) - категория событий
'''
student_action - Событие, совершённое студентом
auth_event - Всё, что связано с авторизацией/регистрацией
system_event - Внутреннее системное событие
email_event - Событие, связанное с отправкой почты
error_event - общая ошибка
'''

# Конкретное действие/событие (EventType)
'''
описаны в ошибках
'''

# Причина события или ошибки (Reason)



# Функция для FastAPI зависимости — просто возвращает уже созданный продюсер
def get_kafka_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        try:
            # Создаём экземпляр продюсера
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, # Адрес Kafka-брокера
                value_serializer=lambda v: json.dumps(v).encode("utf-8"), # сериализация в JSON
                retries=3,       # попытки повторной отправки
                linger_ms=5      # ждёт 5 мс перед отправкой (может собрать несколько сообщений в одну партию)
            )
            print("[Kafka] Producer initialized")
        except Exception as e:
            print(f"[Kafka] Failed to initialize producer: {e}")
            _producer = None
    return _producer


# Функция логирования действий в Kafka
def send_log(StudentID: int, StudentLogin: str, action: str, details: dict = None):
    producer = get_kafka_producer()
    if not producer:
        logging.warning("[Kafka] Producer not available. Log not sent.")
        return
    message  = {
        "action_type": "student_action",   # Лучше использовать четкий тип для логов
        "timestamp": datetime.utcnow().isoformat(),  # Добавим временную метку
        "data": {
            "StudentID": StudentID,
            "StudentLogin": StudentLogin,
            "EventType": action,             # в consumer ты ожидаешь EventType, а не просто action
            "DescriptionEvent": details.get("DescriptionEvent") if details else None,
            "Reason": details.get("Reason") if details else None,
            "IPAddress": details.get("IPAddress") if details else None,
            "UserAgent": details.get("UserAgent") if details else None,
            "Metadata": details.get("Metadata") if details else None,
        }
    }

    try:
        future = producer.send("students.actions", value=message)
        future.get(timeout=1.0)  # ждём максимум 1 секунду ответа от брокера
        #producer.flush()  # Можно опустить, если работает в режиме batch
        print(f"[Kafka] Log sent: {message}")
        logging.info(f"[Kafka] Log sent: {message}")
    except KafkaError as e:
        logging.warning(f"[Kafka] Failed to send log (KafkaError): {e}")
    except Exception as e:
        print(f"[Kafka] Failed to send log: {e}")



# Функция отправки email через Kafka
def send_email_event(event_type: str, email: str, subject: str, template: str, data: dict):
    producer = get_kafka_producer()
    if not producer:
        logging.warning("[Kafka] Producer not available. Email not sent.")
        return

    message = {
        "event_type": event_type,
        "timestamp": TIME_NOW.isoformat(),
        "email": email,
        "subject": subject,
        "template": template,
        "data": data
    }

    try:
        future = producer.send("email.notifications", value=message)
        future.get(timeout=1.0)
        logging.info(f"[Kafka] Email event sent: {message}")
    except KafkaError as e:
        logging.warning(f"[Kafka] Failed to send email event: {e}")


# пример вызова send_email_event
'''
#Регистрация
send_email_event(
    event_type="email_registration",
    email=user_data.email,
    subject="Подтверждение регистрации",
    template="registration_confirmation",
    data={"confirmation_link": f"https://yourdomain.com/confirm-email?token={token}"}
)
# Сброс пароля
send_email_event(
    event_type="email_reset_password",
    email=user.email,
    subject="Восстановление доступа",
    template="reset_password",
    data={"reset_link": f"https://yourdomain.com/reset-password?token={token}"}
)

# Новости
send_email_event(
    event_type="email_news",
    email=user.email,
    subject="Наши новости!",
    template="newsletter",
    data={"title": "Обновления в системе", "body": "Мы добавили новые фичи..."}
)
'''