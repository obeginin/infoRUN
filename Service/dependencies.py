from Database import SessionLocal, LogSessionLocal # ссылаемся на файл с конфигом БД
from main import kafka_producer

# Dependency.py
'''файл с зависимостями '''

'''Зависимость для получения основной базы данных'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''Зависимость для получения базы данных с логами'''
def get_log_db():
    db = LogSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_producer_dep():
    return kafka_producer