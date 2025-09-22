import subprocess
import sys

# worker
def run_celery():

    cmd = [
        sys.executable, "-m", "celery",
        "-A", "Celery_worker.worker",
        "worker",
        "--loglevel=info",
        "--pool=solo"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    run_celery()

'''Запуск через cmd worker и flower'''
# celery -A Celery_worker.worker worker --loglevel=info --pool=solo
# python -m celery -A Celery_worker.worker flower --broker=redis://10.0.2.4:6379/0

