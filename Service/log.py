# log.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import datetime
from config import LOG_DIR, ARCHIVE_LOG_DIR, LOG_FILE, LOG_PATH, LOG_LEVEL
import time
import shutil
import re

class ArchiveHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        # Дождемся, пока файл освободится (можно увеличить, если не помогает)
        time.sleep(0.2)

        # Найдём последний созданный лог-файл по шаблону
        log_dir = os.path.dirname(self.baseFilename)
        base_name = os.path.basename(self.baseFilename)

        # Ожидаем: app.2025-07-31_12-12.log
        pattern = re.compile(re.escape(base_name) + r'\.\d{4}-\d{2}-\d{2}_\d{2}-\d{2}\.log$')
        candidates = [f for f in os.listdir(log_dir) if pattern.fullmatch(f)]

        if not candidates:
            logging.getLogger().warning("Не найден ни один файл для архивации")
            return

        # Найдём самый новый файл (на всякий случай, если их несколько)
        full_paths = [os.path.join(log_dir, f) for f in candidates]
        full_paths.sort(key=os.path.getmtime, reverse=True)
        old_log_path = full_paths[0]

        try:
            dest = os.path.join(ARCHIVE_LOG_DIR, os.path.basename(old_log_path))
            shutil.move(old_log_path, dest)
            logging.getLogger().info(f"Лог перемещён в архив: {dest}")
        except Exception as e:
            logging.getLogger().error(f"Ошибка при перемещении лог-файла: {e}")

def setup_logging():
    # Удалим старые обработчики, если есть
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = ArchiveHandler(
        LOG_PATH, 
        when = "midnight", 
        interval = 1, 
        backupCount = 30, 
        encoding = 'utf-8')

    handler.suffix = "%Y-%m-%d.log"  # итог: app.2025-07-31.log
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}\.log$")


    # для проверка каждую минуту
    '''    handler = ArchiveHandler(
            LOG_PATH,
            when="M",  # M = minute
            interval=1,  # каждые 1 минуту
            backupCount=5,
            encoding='utf-8'
        )
    handler.suffix = "%Y-%m-%d_%H-%M.log"  # итог: app.2025-07-31_12-12.log
    handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}\.log$")
        '''
    # Конвертируем строку уровня логов в числовое значение
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
# настраивает логирование:
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[handler, logging.StreamHandler()]
    )

    logging.info(f"Логирование по дням инициализировано. Уровень: {LOG_LEVEL.upper()}")