from kafka import KafkaProducer
import json
import logging
logger = logging.getLogger(__name__)

# Создание Kafka Producer'а
producer = KafkaProducer(
    bootstrap_servers='10.0.2.4:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Функция логирования действий
def send_log(action: str, StudentID: int, details: dict = None):
    data = {
        "StudentID": StudentID,
        "action": action,
        "details": details or {},
    }
    print("Отправляем лог в Kafka:", data)
    logging.info("Отправляем лог в Kafka:", data)
    producer.send("students.actions", value=data)
    producer.flush()