import subprocess

#subprocess.run(["python", "main.py"])
# Запуск сервера через subprocess (Не работает --reload)
#subprocess.run(["uvicorn", "main:app", "--reload", "--port", "9000"])

subprocess.run([
    "uvicorn",
    "Service.main:app",
    "--host", "0.0.0.0",
    "--port", "9000",
    "--reload"
])
# ручной запуск сервера через консоль
# uvicorn Main:app --reload --port 9000