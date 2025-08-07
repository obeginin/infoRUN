import subprocess
import sys


def run_celery():
    cmd = [
        sys.executable, "-m", "celery",
        "-A", "Celery_worker.email_worker",
        "flower",
        "--port=5555"
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    run_celery()

