import subprocess
import sys
import os
import time
from utils.time import TIME_NOW
from pathlib import Path

# Корень проекта (где находится сам файл run_all.py)
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)  # Устанавливаем текущую директорию

# Добавляем BASE_DIR в sys.path, чтобы работали импорты
sys.path.append(str(BASE_DIR))


REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")


LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
# логирование для запуска
startup_log_path = os.path.join("logs", "startup.log")
STARTUP_LOG = open("logs/startup.log", "a", encoding="utf-8") # используем один файл лога для запуска всех приложений
def log_separator(name: str):
    timestamp = TIME_NOW()
    STARTUP_LOG.write(f"\n\n=== [{name} START] === {timestamp}\n")
    STARTUP_LOG.flush()  # Сразу записать в файл

PID_DIR = BASE_DIR / "pids"
PID_DIR.mkdir(exist_ok=True)
# функция для сохранения id запущенных процессов
def save_pid(proc, name):
    with open(PID_DIR / f"{name}.pid", "w") as f:
        f.write(str(proc.pid))

def run_uvicorn():
    log_separator("UVICORN")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "Service.main:app",
        "--host", "0.0.0.0",
        "--port", "9000"
    ], stdout=STARTUP_LOG, stderr=subprocess.STDOUT) # Логирование для запуска uvicorn

def run_celery_worker():
    log_separator("CELERY WORKER")
    return subprocess.Popen([
        sys.executable, "-m", "celery",
        "-A", "Celery_worker.worker",
        "worker",
        "--loglevel=info",
        "--pool=solo"
    ], stdout=STARTUP_LOG, stderr=subprocess.STDOUT)

def run_flower():
    log_separator("FLOWER")
    return subprocess.Popen([
        sys.executable,
        "-m", "celery",
        "-A", "Celery_worker.worker",
        "flower",
        f"--broker={REDIS_BROKER_URL}"
    ], stdout=STARTUP_LOG, stderr=subprocess.STDOUT)

def run_kafka():
    log_separator("KAFKA CONSUMER")
    return subprocess.Popen([
        sys.executable,
        "kafka_consumer/consumer.py"
    ], stdout=STARTUP_LOG, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    print("[START] Запускаем все компоненты...")

    uvicorn_proc = run_uvicorn()
    save_pid(uvicorn_proc, "uvicorn")

    celery_proc = run_celery_worker()
    save_pid(celery_proc, "celery_worker")

    flower_proc = run_flower()
    save_pid(flower_proc, "flower")

    kafka_proc = run_kafka()
    save_pid(kafka_proc, "kafka_consumer")

    print("[INFO] Все сервисы запущены. PID сохранены.")

'''uvicorn'''
# http://localhost:9000/
'''Flower (Celery Dashboard)'''
# http://localhost:5555/
'''kafka'''
# http://10.0.2.4:8080/