# log.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import datetime
from utils.config import settings
import time
import shutil
import re
from pathlib import Path

def setup_logging(log_file: str = "app.log", archive_dir: Path = None):
    log_dir = settings.LOG_DIR
    log_path = log_dir / log_file
    archive_dir = archive_dir or settings.ARCHIVE_LOG_DIR
    archive_dir.mkdir(parents=True, exist_ok=True)

    class ArchiveHandler(TimedRotatingFileHandler):
        def __init__(self, *args, archive_dir: Path, **kwargs):
            self.archive_dir = archive_dir
            self._rolled_over = False  # <--- флаг
            super().__init__(*args, **kwargs)

        def doRollover(self):
            if self._rolled_over:
                return  # уже ротация была
            self._rolled_over = True

            if self.stream:
                self.stream.close()
                self.stream = None

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-00")
            base_name = Path(self.baseFilename).stem
            archive_filename = f"{base_name}.{timestamp}.log"
            archive_path = self.archive_dir / archive_filename

            try:
                shutil.copy2(self.baseFilename, archive_path)
                with open(self.baseFilename, "w", encoding="utf-8"):
                    pass
                print(f"Лог архивирован: {archive_path}")
            except Exception as e:
                print(f"Ошибка архивации: {e}")

            self.mode = 'a'
            self.stream = self._open()
            self._rolled_over = False  # сброс флага для следующей ротации

    handler = ArchiveHandler(
        filename=str(log_path),
        when="midnight",           # или "M" для тестов каждую минуту midnight
        interval=1,
        backupCount=30,
        encoding="utf-8",
        archive_dir=archive_dir
    )

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[handler, logging.StreamHandler()]
    )

    logging.info(f"Логирование инициализировано. Лог: {log_path}, Архив: {archive_dir}")
