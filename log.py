# log.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import datetime
from config import LOG_DIR, ARCHIVE_DIR, LOG_FILE, LOG_PATH


class ArchiveHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        # Получаем имя последнего лог-файла
        # Вычислим имя старого лог-файла
        rollover_time = self.rolloverAt - self.interval
        rollover_date = datetime.datetime.fromtimestamp(rollover_time).strftime(self.suffix)
        old_log = f"{self.baseFilename}.{rollover_date}"

        if os.path.exists(old_log):
            dest = os.path.join(ARCHIVE_DIR, os.path.basename(old_log))
            os.rename(old_log, dest)

def setup_logging():
    # Удалим старые обработчики, если есть
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = ArchiveHandler(
        LOG_PATH, when = "midnight", interval = 1, backupCount = 30, encoding = 'utf-8')

    handler.suffix = "%Y-%m-%d"  # добавит дату к файлу, например: app.log.2025-05-19

# настраивает логирование:
    logging.basicConfig(
        level = logging.INFO,
        encoding="utf-8",
        format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers = [
            handler,
            logging.StreamHandler() #вывод логов также дублируется в консоль.
            ]
        )

    logging.info("Логирование по дням инициализировано.")