from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from Service.producer import get_kafka_producer
# Database.py
'''файл снастройкой подключения к базе'''


load_dotenv()  # загрузить .env в окружение

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
# Строка подключения для pymssql
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # для логов SQL-запросов, можно выключить
    future=True,
)

# Фабрика для создания асинхронных сессий

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


Base = declarative_base() # базовый класс, от которого будут наследоваться все модели таблиц в SQLAlchemy.

'''Зависимость для получения основной базы данных'''
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session






'''
DB_NAME_LOG = os.getenv("DB_NAME_LOG")
DB_HOST_LOG = os.getenv("DB_HOST_LOG")
DB_USER_LOG = os.getenv("DB_USER_LOG")
DB_PASS_LOG = os.getenv("DB_PASS_LOG")
LOG_DATABASE_URL = (f"mssql+pyodbc://{DB_USER_LOG}:{DB_PASS_LOG}@{DB_HOST_LOG}/{DB_NAME_LOG}"
                    f"?driver=ODBC+Driver+18+for+SQL+Server"
                    "&TrustServerCertificate=yes")
log_engine = create_engine(LOG_DATABASE_URL)
LogSessionLocal = sessionmaker(bind=log_engine)

#Зависимость для получения базы данных с логами
def get_log_db():
    db = LogSessionLocal()
    try:
        yield db
    finally:
        db.close()'''

def get_producer_dep():
    return get_kafka_producer()