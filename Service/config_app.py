from dotenv import load_dotenv
import os
from pathlib import Path


from fastapi.templating import Jinja2Templates
from utils.config import TIME_NOW
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

LOG_FILE = os.getenv("LOG_FILE")

'''Уровень логирования'''
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")




