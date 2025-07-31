import subprocess
import sys

def run_celery():
    cmd = [
        sys.executable, "-m", "celery",
        "-A", "Service.celery_tasks.email_worker",
        "worker",
        "--loglevel=info",
        "--pool=solo"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    run_celery()