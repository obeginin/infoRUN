import os
import signal
from pathlib import Path
import subprocess
import io
import sys
import psutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
PID_DIR = BASE_DIR / "pids"

import psutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PID_DIR = BASE_DIR / "pids"

def stop_process_by_pid_file(name):
    pid_file = PID_DIR / f"{name}.pid"
    if not pid_file.exists():
        print(f"No PID file for {name}")
        return

    with open(pid_file) as f:
        pid = int(f.read())

    if psutil.pid_exists(pid):
        try:
            parent = psutil.Process(pid)
            # убиваем всех дочерних процессов рекурсивно
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            print(f"Process {name} with PID {pid} and its children terminated.")
        except Exception as e:
            print(f"Failed to terminate {name} with PID {pid}: {e}")
    else:
        print(f"Process {name} with PID {pid} does not exist.")
    # удаляем PID файл
    pid_file.unlink()

def stop_frontend_process():
    """Дополнительно убиваем все node/npm процессы, связанные с папкой client"""
    client_path = str(BASE_DIR / "client").lower()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = (proc.info['name'] or '').lower()
            cmdline_list = proc.info['cmdline'] or []
            cmdline = ' '.join(cmdline_list).lower()
            if ('node' in name or 'npm' in name) and client_path in cmdline:
                proc.kill()
                print(f"Killed frontend process PID {proc.pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    services = ["uvicorn", "celery_worker", "flower", "kafka_consumer", "frontend"]
    for service in services:
        if service == "frontend":
            stop_frontend_process()
        else:
            stop_process_by_pid_file(service)

    print("[INFO] Все сервисы остановлены.")

