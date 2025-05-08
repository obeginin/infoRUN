import subprocess

#subprocess.run(["python", "main.py"])
# Запуск сервера через subprocess (Не работает --reload)
#subprocess.run(["uvicorn", "main:app", "--reload", "--port", "9000"])

subprocess.run([
    "uvicorn",
    "main:app",
    "--host", "localhost",
    "--port", "9000",
    "--reload"
])
# ручной запуск сервера через консоль
# uvicorn Main:app --reload --port 9000