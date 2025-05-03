import subprocess

# Запуск сервера через subprocess
subprocess.run(["uvicorn", "main:app", "--port", "9000"])

# ручной запуск сервера через консоль
# uvicorn Main:app --reload --port 9000