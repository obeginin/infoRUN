from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
# Database.py
'''файл снастройкой подключения к базе'''


load_dotenv()  # загрузить .env в окружение

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
# Строка подключения для pymssql
DATABASE_URL = (
    f"mssql+pyodbc://{DB_HOST}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes")
engine = create_engine(DATABASE_URL) # функция create_engine создаёт объект соединения с базой данных.

#фабрика для создания сессий подключения к базе (через неё мы будем выполнять запросы).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # базовый класс, от которого будут наследоваться все модели таблиц в SQLAlchemy.



'''
Стандартная проверка подключения к БД
Пример запроса для проверки подключения
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Успешное подключение! ✅ Результат:", result.scalar())
except Exception as e:
    print("❌ Ошибка подключения:", e)

'''
