# log.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

def setup_logging():
    # Удалим старые обработчики, если есть
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=5, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.info("Логирование инициализировано.")