@echo off
chcp 65001 > nul
echo [START] Активируем виртуальное окружение...
call C:\infoRUN\Service\.venv\Scripts\activate.bat

echo [INFO] Запускаем управляющий скрипт run_project.py
python C:\infoRUN\run_project.py


pause

