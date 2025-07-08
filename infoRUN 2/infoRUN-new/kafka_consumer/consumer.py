# Главный consumer читает из kafka и передает в роут
from router import handle_action
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from kafka import KafkaConsumer
from contextlib import contextmanager

# Подключение к базе данных SQL Server
DATABASE_URL = "mssql+pyodbc://sa:1234@localhost/LogDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Подключение к базе данных успешно:", result.scalar())
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)

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
        bootstrap_servers='10.0.2.4:9092',
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



