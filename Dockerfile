# Используем официальный Python образ
FROM python:3.12-slim

# Указываем переменные окружения (опционально)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/infoRUN_Postgres

# Устанавливаем рабочую директорию
WORKDIR /infoRUN_Postgres

# Установка зависимостей системы (gcc нужен для некоторых Python-пакетов)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

EXPOSE 9000

# Команда для запуска приложения
CMD ["uvicorn", "Service.main:app", "--host", "0.0.0.0", "--port", "9000"]
