from kafka import KafkaProducer
from dotenv import load_dotenv
import json
import logging
import os
logger = logging.getLogger(__name__)

load_dotenv()
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

# Создание Kafka Producer'а
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Функция логирования действий
def send_log(producer, StudentID: int, StudentLogin: str, action: str, details: dict = None):
    data = {
        "action_type": "student_action",   # Лучше использовать четкий тип для логов
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
    print("Отправляем лог в Kafka:", data)
    logging.info("Отправляем лог в Kafka:", data)
    producer.send("students.actions", value=data)
    producer.flush()