from datetime import datetime
from pytz import timezone

def TIME_NOW():
    now_moscow = datetime.now(timezone("Europe/Moscow")) # Убрать таймзону, но сохранить локальное время
    return now_moscow.replace(tzinfo=None)  # без +03:00