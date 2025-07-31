
from dotenv import load_dotenv
import os
from pathlib import Path

# надо объединить конфиги
load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
#LOG_DIR = Path(os.getenv("LOG_DIR"))
LOG_FILE = os.getenv("LOG_FILE")
# Получаем из env, если есть, иначе дефолт — папка archive внутри LOG_DIR
archive_dir_env = os.getenv("ARCHIVE_LOG_DIR")
if archive_dir_env:
    ARCHIVE_LOG_DIR = Path(archive_dir_env).resolve()
else:
    ARCHIVE_LOG_DIR = LOG_DIR / "archive"
os.makedirs(LOG_DIR, exist_ok=True) # создает каталог, если его нет.
os.makedirs(ARCHIVE_LOG_DIR, exist_ok=True)



'''Уровень логирования'''
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")