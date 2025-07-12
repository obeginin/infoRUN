from kafka import KafkaProducer
from dotenv import load_dotenv
import json
from datetime import datetime
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


# Функция логирования действий
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
        producer.send("students.actions", value=message)
        producer.flush()  # Можно опустить, если работает в режиме batch
        print(f"[Kafka] Log sent: {message}")
        logging.info(f"[Kafka] Log sent: {message}")
    except Exception as e:
        print(f"[Kafka] Failed to send log: {e}")


