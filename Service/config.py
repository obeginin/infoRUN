from dotenv import load_dotenv
import os
from pathlib import Path

from datetime import datetime
from pytz import timezone
from fastapi.templating import Jinja2Templates
#from config import UPLOAD_IMAGE_DIR, UPLOAD_SOLUTION_DIR, UPLOAD_FILES_DIR, UPLOAD_STUDENTS_IMAGE_DIR
load_dotenv() # загружаем переменные из файла .env


'''подключаем токен из конфига .env'''
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # второе значение дефолт
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 300))


'''подключаем папки из конфига .env'''
UPLOAD_IMAGE_DIR = Path(os.getenv("UPLOAD_IMAGE_DIR"))
UPLOAD_SOLUTION_DIR = Path(os.getenv("UPLOAD_SOLUTION_DIR"))
UPLOAD_FILES_DIR = Path(os.getenv("UPLOAD_FILES_DIR"))
UPLOAD_STUDENTS_IMAGE_DIR = Path(os.getenv("UPLOAD_STUDENTS_IMAGE_DIR"))
UPLOAD_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_SOLUTION_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_FILES_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_STUDENTS_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES_DIR = "templates"

LOG_DIR = Path(os.getenv("LOG_DIR", "logs.log"))
LOG_FILE = Path(os.getenv("LOG_FILE", "app")) #имя лог-файла.
ARCHIVE_LOG_DIR = Path(os.getenv("ARCHIVE_LOG_DIR", LOG_DIR / "archive"))
os.makedirs(LOG_DIR, exist_ok=True) # создает каталог, если его нет.
os.makedirs(ARCHIVE_LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

'''Уровень логирования'''
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

#время по москве
now_moscow = datetime.now(timezone("Europe/Moscow"))
# Убрать таймзону, но сохранить локальное время
TIME_NOW = now_moscow.replace(tzinfo=None)


