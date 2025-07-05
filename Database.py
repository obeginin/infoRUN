from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
# Database.py
'''файл снастройкой подключения к базе'''


load_dotenv()  # загрузить .env в окружение

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
# Строка подключения для pymssql
DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    #f"mssql+pyodbc://{DB_HOST}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    #"&trusted_connection=yes"
    "&TrustServerCertificate=yes")
engine = create_engine(DATABASE_URL) # функция create_engine создаёт объект соединения с базой данных.

#фабрика для создания сессий подключения к базе (через неё мы будем выполнять запросы).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # базовый класс, от которого будут наследоваться все модели таблиц в SQLAlchemy.

DB_NAME_LOG = os.getenv("DB_NAME_LOG")
DB_HOST_LOG = os.getenv("DB_HOST_LOG")
DB_USER_LOG = os.getenv("DB_USER_LOG")
DB_PASS_LOG = os.getenv("DB_PASS_LOG")
LOG_DATABASE_URL = (f"mssql+pyodbc://{DB_USER_LOG}:{DB_PASS_LOG}@{DB_HOST_LOG}/{DB_NAME_LOG}"
                    f"?driver=ODBC+Driver+18+for+SQL+Server"
                    "&TrustServerCertificate=yes")
log_engine = create_engine(LOG_DATABASE_URL)
LogSessionLocal = sessionmaker(bind=log_engine)
