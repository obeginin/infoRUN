# Главный consumer читает из kafka и передает в роут
from router import handle_action
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from kafka import KafkaConsumer
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
# переменные для подключения к БД с логами
DB_HOST_LOG=os.getenv("DB_HOST_LOG")
DB_NAME_LOG=os.getenv("DB_NAME_LOG")
DB_USER_LOG=os.getenv("DB_USER_LOG")
DB_PASS_LOG=os.getenv("DB_PASS_LOG")


# Подключение к базе данных SQL Server
DATABASE_URL =f"mssql+pyodbc://{DB_USER_LOG}:{DB_PASS_LOG}@{DB_HOST_LOG}/{DB_NAME_LOG}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Подключение к базе данных с логами успешно:", result.scalar())
    except Exception as e:
        print("Ошибка подключения к базе данных с логами:", e)

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def consume_messages():
    consumer = KafkaConsumer(
        'students.actions',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='main-consumer-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    try:
        for msg in consumer:
            message = msg.value
            print(f"Получено сообщение: {message}")
            with get_db_session() as db:
                try:
                    handle_action(message, db)
                except Exception as e:
                    print(f"Ошибка обработки сообщения: {e}")
    except KeyboardInterrupt:
        print("Остановлено пользователем")



if __name__ == "__main__":
    test_db_connection()
    consume_messages()



