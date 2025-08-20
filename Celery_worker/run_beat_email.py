import subprocess
import sys

# worker
def run_celery_beat():

    cmd = [
        sys.executable, "-m", "celery",
        "-A", "Celery_worker.email_worker",
        "beat",
        "--loglevel=info"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    run_celery_beat()
