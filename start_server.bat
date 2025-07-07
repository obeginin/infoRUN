@echo off
chcp 65001 > nul
rem Скрипт для автоматического запуска
cd /d C:\New\
echo ------------------ >> logs\logs.txt
echo Запуск: %date% %time% >> logs.txt
C:\New\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 9000 --reload >> logs.txt 2>&1

pause

