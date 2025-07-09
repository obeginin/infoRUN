from kafka import KafkaProducer
from dotenv import load_dotenv
import json
import datetime
import logging
import os
logger = logging.getLogger(__name__)

load_dotenv()
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

# Создание Kafka Producer
def get_kafka_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, # Адрес Kafka-брокера
        value_serializer=lambda v: json.dumps(v).encode("utf-8"), # сериализация в JSON
        retries=3,       # попытки повторной отправки
        linger_ms=5      # ждёт 5 мс перед отправкой (может собрать несколько сообщений в одну партию)
    )
    return producer

# Функция логирования действий
def send_log(producer: KafkaProducer, StudentID: int, StudentLogin: str, action: str, details: dict = None):
    message  = {
        "action_type": "student_action",   # Лучше использовать четкий тип для логов
        "timestamp": datetime.utcnow().isoformat(),  # Добавим временную метку
        "data": {
            "StudentID": StudentID,
            "StudentLogin": StudentLogin,
            "EventType": action,             # в consumer ты ожидаешь EventType, а не просто action
            "DescriptionEvent": details.get("DescriptionEvent") if details else None,
            "IPAddress": details.get("IPAddress") if details else None,
            "UserAgent": details.get("UserAgent") if details else None,
            "Metadata": details.get("Metadata") if details else None,
        }
    }

    try:
        producer.send("students.actions", json.dumps(message).encode("utf-8"))
        producer.flush()  # Можно опустить, если работает в режиме batch
        print(f"[Kafka] Log sent: {message}")
        logging.info(f"[Kafka] Log sent: {message}")
    except Exception as e:
        print(f"[Kafka] Failed to send log: {e}")


