import os
import signal
from pathlib import Path
import subprocess
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
PID_DIR = BASE_DIR / "pids"

def stop_process(name):
    pid_file = PID_DIR / f"{name}.pid"
    if pid_file.exists():
        with open(pid_file) as f:
            pid = int(f.read())
        try:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
            print(f"Process {name} with PID {pid} terminated by taskkill.")
        except subprocess.CalledProcessError:
            print(f"Failed to terminate process {name} with PID {pid}.")
        pid_file.unlink()

if __name__ == "__main__":
    for proc_name in ["uvicorn", "celery_worker", "flower", "kafka_consumer"]:
        stop_process(proc_name)